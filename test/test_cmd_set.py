from mocker import MockerTestCase, ANY

from common.models import AdminVariable
from bot.commands import Command
from bot.users import User

_var = "plop"
_val = "foo"
_admin_sender = "admin@example.com"
_admin_cmd = "set --admin %s %s" % (_var, _val)
_user_sender = "john.doe@example.com"
_user_cmd = "set %s %s" % (_var, _val)

def _buildMsg(mocker, sender, cmd):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(sender)

    fake_msg.body
    mocker.result(cmd)

    fake_msg.reply(ANY)

    return fake_msg

class TestSet(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender, _user_cmd)
        self.mocker.replay()

    def testSetCmd(self):
        Command.dispatch(self.user_msg)
        user = User(_user_sender)
        val = user.getVariable(_var)
        self.assertEqual(val, _val)

class TestAdminSet(MockerTestCase):

    def setUp(self):
        self.admin_msg = _buildMsg(self.mocker, _admin_sender, _admin_cmd)
        self.mocker.replay()

    def testSetCmd(self):
        user = User(_admin_sender)
        user.makeAdmin()
        Command.dispatch(self.admin_msg)
        var = AdminVariable(_var)
        self.assertEqual(var.get(), _val)
