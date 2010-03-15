from common.models import DbUserRole, UserVariable
from google.appengine.ext import db
from google.appengine.api import users as gusers

class User(object):

    def __init__(self, email):
        self.email = email

        user = gusers.User(email)
        user_role = db.GqlQuery("SELECT * FROM DbUserRole WHERE account = :1", user).get()
        if user_role is None:
            user_role = DbUserRole(role=DbUserRole._USER_ROLE,
                                   account=user)
            user_role.put()
        self.db_role = user_role

    def delete(self):
        self.db_role.delete()

    def isAdmin(self):
        return self.db_role.role == DbUserRole._ADMIN_ROLE

    def makeAdmin(self):
        self.db_role.role = DbUserRole._ADMIN_ROLE
        self.db_role.put()

    def __repr__(self):
        return self.db_role.account.nickname()

    # Commodity accessors for UserVariable objects
    def getVariable(self, name, *args, **kwds):
        """see UserVariable.get() for arguments"""
        return UserVariable(self, name).get(*args, **kwds)

    def setVariable(self, name, *args, **kwds):
        """see UserVariable.set() for arguments"""
        return UserVariable(self, name).set(*args, **kwds)

    def deleteVariable(self, name, *args, **kwds):
        """see UserVariable.delete() for arguments"""
        return UserVariable(self, name).delete(*args, **kwds)
