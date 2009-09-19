from bot.commands import PrefixCommand

class Echo(PrefixCommand):

    PREFIX = 'echo'

    def run(self):
        return self.args[1]

    def tokenizeArguments(self, txt):
        return [txt[:len(self.PREFIX)], txt[len(self.PREFIX):].lstrip()]
