from common.models import DbUserRole
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

    def isAdmin(self):
        return self.db_role.role == DbUserRole._ADMIN_ROLE

    def makeAdmin(self):
        self.db_role.role = DbUserRole._ADMIN_ROLE
        self.db_role.put()

    def __repr__(self):
        return self.db_role.account.nickname()
