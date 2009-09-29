from google.appengine.ext import db

class UserRole(db.Model):
    _ADMIN_ROLE = "admin"
    _USER_ROLE = "user"
    account = db.UserProperty()
    role = db.StringProperty(required=True, choices=set([_ADMIN_ROLE, _USER_ROLE]))

class AdminVariable(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()

class UserVariable(db.Model):
    name = db.StringProperty()
    value = db.StringProperty()
