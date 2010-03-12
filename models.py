from google.appengine.ext import db
from google.appengine.api.datastore_errors import BadQueryError

class DbUserRole(db.Model):
    _ADMIN_ROLE = "admin"
    _USER_ROLE = "user"
    account = db.UserProperty()
    role = db.StringProperty(required=True, choices=set([_ADMIN_ROLE, _USER_ROLE]))

class DbAdminVariable(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()

class DbUserVariable(db.Model):
    user = db.StringProperty()
    name = db.StringProperty()
    value = db.StringProperty()

class NoSuchVariable(Exception):
    pass

class AbstractMethod(Exception):
    pass

class _Variable(object):

    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return "%s/%s" % (self.__class__, self._name)

    def _getModelObject(self):
        raise AbstractMethod("_getModelObject")

    def _createModelObject(self, value):
        raise AbstractMethod("_createModelObject")

    def get(self, default=None, create=False):
        try:
            res = self._getModelObject().get()
        except BadQueryError, e:
            res = default
            if create:
                self.set(res, create=True)
        return res

    def set(self, value, create=True):
        try:
            mo = self._getModelObject().get()
        except BadQueryError, e:
            mo = None

        if mo is None:
            if not create:
                raise NoSuchVariable(self.__repr__())
            mo = self._createModelObject(value)
        mo.put()

class AdminVariable(_Variable):

    def __init__(self, name):
        _Variable.__init__(self, name)

    def _getModelObject(self):
        return db.GqlQuery("SELECT * FROM DbAdminVariable WHERE name = :1", self._name)

    def _createModelObject(self, value):
        return DbAdminVariable(name=self._name, value=value)

class UserVariable(_Variable):

    def __init__(self, user, name):
        _Variable.__init__(self, name)
        self._user = user

    def __repr__(self):
        return "%s/%s/%s" % (self.__class__, self._user, self._name)

    def _getModelObject(self):
        return db.GqlQuery("SELECT * FROM DbUserVariable WHERE name = :1 and user = :2", self._name, self._user)

    def _createModelObject(self, value):
        obj = DbAdminVariable(user=self._user, name=self._name, value=value)
        return obj
