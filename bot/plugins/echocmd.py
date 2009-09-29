from bot.commands import PrefixCommand

class EchoCmd(PrefixCommand):

    PREFIX = 'echo'

    def run(self):
        return self.args[0]
