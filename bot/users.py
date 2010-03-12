from models import DbUserRole
from google.appengine.ext import db
from google.appengine.api import users as gusers

class User(object):

    def __init__(self, email):
        self.email = email

        try:
            user = gusers.User(email)
            user_role = db.GqlQuery("SELECT * FROM DbUserRole WHERE account = :1", user).get()
            if user_role is None:
                user_role = DbUserRole(role=DbUserRole._USER_ROLE,
                                     account=user)
                user_role.put()
            self.role = user_role.role
        except Exception, e:
            self.role = DbUserRole._USER_ROLE

    def isAdmin(self):
        return self.role == DbUserRole._ADMIN_ROLE

    def __repr__(self):
        return self.email
