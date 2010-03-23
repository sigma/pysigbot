from bot.commands import PrefixCommand

class HelloCmd(PrefixCommand):

    PREFIX = 'hello'

    ADMIN_TPL = "Greetings Master %s. Your wish is my command !"
    USER_TPL = "Greetings %s."

    def run(self):
        if self.sender.isAdmin():
            return self.ADMIN_TPL % (self.sender)
        else:
            return self.USER_TPL % (self.sender)
