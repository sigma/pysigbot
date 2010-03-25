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

    def _getModelObject(self): # pragma nocover
        raise AbstractMethod("_getModelObject")

    def _createModelObject(self, value): # pragma nocover
        raise AbstractMethod("_createModelObject")

    def get(self, default=None, create=False):
        try:
            mo = self._getModelObject()
        except BadQueryError, e: # pragma nocover
            mo = None
        if mo is None:
            mo = self._createModelObject(default)
            if create:
                mo.put()
        return mo.value

    def set(self, value, create=True):
        try:
            mo = self._getModelObject()
        except BadQueryError, e: # pragma nocover
            mo = None

        if mo is None:
            if not create:
                raise NoSuchVariable(self.__repr__())
            mo = self._createModelObject(value)
        mo.value = value
        mo.put()

    def delete(self):
        try:
            mo = self._getModelObject()
        except BadQueryError, e: # pragma nocover
            mo = None
        if mo is not None:
            mo.delete()

class AdminVariable(_Variable):

    def __init__(self, name):
        _Variable.__init__(self, name)

    def _getModelObject(self):
        return db.GqlQuery("SELECT * FROM DbAdminVariable WHERE name = :1", self._name).get()

    def _createModelObject(self, value):
        return DbAdminVariable(name=self._name, value=value)

class UserVariable(_Variable):

    def __init__(self, user, name):
        _Variable.__init__(self, name)
        # store a string in any case, so that user can be a User object, or
        # just it's nickname
        self._user = user.__repr__()

    def __repr__(self):
        return "%s/%s/%s" % (self.__class__, self._user, self._name)

    def _getModelObject(self):
        return db.GqlQuery("SELECT * FROM DbUserVariable WHERE name = :1 and user = :2", self._name, self._user).get()

    def _createModelObject(self, value):
        return DbUserVariable(user=self._user, name=self._name, value=value)
