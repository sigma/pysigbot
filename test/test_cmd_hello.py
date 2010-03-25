from mocker import MockerTestCase

from bot.commands import Command
from bot.plugins.hellocmd import HelloCmd
from bot.users import User

_admin_sender = "admin@example.com"
_user_sender = "john.doe@example.com"
_cmd = "hello bot !"
_cmd_alt = "HeLLo bot !"

def _buildMsg(mocker, sender, cmd, reply):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(sender)
    mocker.count(0, None)

    fake_msg.body
    mocker.result(cmd)
    mocker.count(0, None)

    fake_msg.reply(reply)

    return fake_msg

class TestUserHello(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender, _cmd,
                                  HelloCmd.USER_TPL % (_user_sender))
        self.mocker.replay()

    def testHelloCmd(self):
        Command.dispatch(self.user_msg)

class TestCaseHello(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender, _cmd_alt,
                                  HelloCmd.USER_TPL % (_user_sender))
        self.mocker.replay()

    def testHeLLoCmd(self):
        Command.dispatch(self.user_msg)

class TestAdminHello(MockerTestCase):

    def setUp(self):
        self.admin_msg = _buildMsg(self.mocker, _admin_sender, _cmd,
                                  HelloCmd.ADMIN_TPL % (_admin_sender))
        self.mocker.replay()

    def testSetCmd(self):
        user = User(_admin_sender)
        user.makeAdmin()
        Command.dispatch(self.admin_msg)

for cls in [TestUserHello, TestCaseHello, TestAdminHello]:
    cls.status = "stable"
    cls.component = "plugins"
    cls.plugin = "hello"
