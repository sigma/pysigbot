from google.appengine.api import xmpp, users
from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from models import UserRole

class AdminHandler(webapp.RequestHandler):
    def get(self):
        user = users.GetCurrentUser()

        user_role = db.GqlQuery("SELECT * FROM UserRole WHERE account = :1", user).get()
        if user_role is not None:
            u.role = UserRole._ADMIN_ROLE
            u.put()
        else:
            u = UserRole(role=UserRole._ADMIN_ROLE,
                         account=user)
            u.put()

        self.response.out.write("""Hello, %s. You're now defined as '%s'""" %
                                (user.nickname(), u.role))

application = webapp.WSGIApplication([('/admin/', AdminHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
