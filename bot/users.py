from models import UserRole
from google.appengine.ext import db
from google.appengine.api import users as gusers

class User(object):

    def __init__(self, email):
        self.email = email

        try:
            user = gusers.User(email)
            user_role = db.GqlQuery("SELECT * FROM UserRole WHERE account = :1", user).get()
            if user_role is None:
                user_role = UserRole(role=UserRole._USER_ROLE,
                                     account=user)
                user_role.put()
            self.role = user_role.role
        except Exception, e:
            self.role = UserRole._USER_ROLE

    def isAdmin(self):
        return self.role == UserRole._ADMIN_ROLE

    def __repr__(self):
        return self.email
