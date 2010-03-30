from bot.users import User

class Command(object):

    COMMAND_NOT_FOUND_MSG = "Need some help finding your words?"
    COMMAND_NO_ANSWER_MSG = "Ack !"

    @classmethod
    def dispatch(cls, message):
        for c in cls.__subclasses__():
            inst = c.accept(message.body, message.sender)
            if inst is not None and hasattr(inst, 'run'):
                answer = inst.run()
                if answer is not None:
                    if type(answer) is list:
                        for line in answer:
                            message.reply(line)
                    else:
                        message.reply(answer)
                else:
                    message.reply(cls.COMMAND_NO_ANSWER_MSG)
                return
        message.reply(cls.COMMAND_NOT_FOUND_MSG)

    @classmethod
    def accept(cls, txt, sender): # pragma nocover
        pass

    def __init__(self, txt, sender):
        self.args = self.tokenizeArguments(txt)
        self.sender = self.getSender(sender)

    def tokenizeArguments(self, txt):
        return txt.split()

    def getSender(self, sender):
        return User(sender.partition("/")[0])

    def run(self): # pragma nocover
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
