from mocker import MockerTestCase

from bot.commands import Command
from bot.plugins.hellocmd import HelloCmd
from bot.users import User

_admin_sender = "admin@example.com"
_user_sender = "john.doe@example.com"
_msg = "foo bar baz !"
_cmd = "echo %s" % (_msg)

def _buildMsg(mocker, sender):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(sender)
    mocker.count(0, None)

    fake_msg.body
    mocker.result(_cmd)
    mocker.count(0, None)

    fake_msg.reply(_msg)

    return fake_msg

class TestUserHello(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender)
        self.mocker.replay()

    def testEchoCmd(self):
        Command.dispatch(self.user_msg)
