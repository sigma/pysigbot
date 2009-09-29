from bot.users import User

class Command(object):

    @classmethod
    def dispatch(cls, message):
        for c in cls.__subclasses__():
            inst = c.accept(message.body, message.sender)
            if inst is not None:
                answer = inst.run()
                if answer is not None:
                    if type(answer) is list:
                        for line in answer:
                            message.reply(line)
                    else:
                        message.reply(answer)
                else:
                    message.reply("Ack !")
                return
        message.reply("Need some help finding your words?")

    @classmethod
    def accept(cls, txt, sender):
        pass

    def __init__(self, txt, sender):
        self.args = self.tokenizeArguments(txt)
        self.sender = self.getSender(sender)

    def tokenizeArguments(self, txt):
        return txt.split()

    def getSender(self, sender):
        return User(sender.partition("/")[0])

    def run(self):
        pass

class PrefixCommand(Command):

    PREFIX = None

    @classmethod
    def accept(cls, txt, sender):
        if cls.PREFIX is None:
            for c in cls.__subclasses__():
                inst = c.accept(txt, sender)
                if inst is not None:
                    return inst
            return None
        pref = cls.PREFIX.lower()
        cmd, sep, rest = txt.partition(' ')
        rest = rest.strip()
        if cmd.lower() == pref:
            for c in cls.__subclasses__():
                inst = c.accept(rest, sender)
                if inst is not None:
                    return inst
            return cls(rest, sender)
        else:
            return None

    def tokenizeArguments(self, txt):
        return [txt]

from bot.plugins import *

class MessageStub(object):

    def __init__(self, body, sender):
        self.body = body
        self.sender = sender

    def reply(self, msg):
        print msg
