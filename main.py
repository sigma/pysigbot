from google.appengine.api import xmpp
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from bot.commands import Command

class XMPPHandler(webapp.RequestHandler):
  def post(self):
    message = xmpp.Message(self.request.POST)
    Command.dispatch(message)

application = webapp.WSGIApplication([('/_ah/xmpp/message/chat/', XMPPHandler)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
