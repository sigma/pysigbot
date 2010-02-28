from google.appengine.ext import db
from google.appengine.api.datastore_errors import BadQueryError

from bot.commands import PrefixCommand
from models import UserVariable, AdminVariable

class SetCmd(PrefixCommand):

    PREFIX = 'set'

    def _setVariable(self, cls, name, value):
        try:
            variable = db.GqlQuery("SELECT * FROM :1 WHERE name = :2", cls.__name__, name).get()
        except BadQueryError, e:
            variable = None
        if variable is None:
            variable = cls(name=name, value=value)
        variable.put()

    def tokenizeArguments(self, txt):
        l = txt.split(None, 1)
        while len(l) < 2:
            l.append(None)
        return l

    def run(self):
        self._setVariable(UserVariable, '%s/%s' % (self.sender, self.args[0]), self.args[1])
        return "Variable '%s' has been set" % (self.args[0])

class SetAdminCmd(SetCmd):

    PREFIX = '--admin'

    def run(self):
        if self.sender.isAdmin():
            self._setVariable(AdminVariable, self.args[0], self.args[1])
            return "Admin variable '%s' has been set" % (self.args[0])
        else:
            return "You must be an admin to do so"
