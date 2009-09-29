from bot.commands import PrefixCommand

class HelloCmd(PrefixCommand):

    PREFIX = 'hello'

    def run(self):
        if self.sender.isAdmin():
            return "Greetings Master %s. Your wish is my command !" % (self.sender)
        else:
            return "Greetings %s." % (self.sender)
