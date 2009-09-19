from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app, login_required

from bot.commands import Command

class XMPPHandler(webapp.RequestHandler):
  def post(self):
    message = xmpp.Message(self.request.POST)
    Command.dispatch(message)

class WebHandler(weapp.RequestHandler):

  @login_required
  def get(self):
    user = users.GetCurrentUser(self)
    self.response.out.write('Hello, ' + user.nickname())

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler),
                                      ('/', WebHandler)],
                                     debug=False)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
