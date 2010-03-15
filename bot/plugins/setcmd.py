from google.appengine.api.datastore_errors import BadQueryError

from bot.commands import PrefixCommand
from common.models import AdminVariable

class SetCmd(PrefixCommand):

    PREFIX = 'set'

    def tokenizeArguments(self, txt):
        l = txt.split(None, 1)
        while len(l) < 2:
            l.append(None)
        return l

    def run(self):
        self.sender.setVariable(self.args[0], self.args[1])
        return "Variable '%s' has been set" % (self.args[0])

class SetAdminCmd(SetCmd):

    PREFIX = '--admin'

    def run(self):
        if self.sender.isAdmin():
            self.sender.setAdminVariable(self.args[0], self.args[1])
            return "Admin variable '%s' has been set" % (self.args[0])
        else:
            return "You must be an admin to do so"
