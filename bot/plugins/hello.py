from bot.commands import PrefixCommand

class Hello(PrefixCommand):

    PREFIX = 'hello'

    def run(self):
        return "Greetings %s!" % (self.sender)
