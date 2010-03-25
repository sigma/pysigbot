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
_incomplete_user_cmd = "set %s" % (_var)

def _buildMsg(mocker, sender, cmd):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(sender)
    mocker.count(0, None)

    fake_msg.body
    mocker.result(cmd)
    mocker.count(0, None)

    fake_msg.reply(ANY)
    mocker.count(0, None)

    return fake_msg

class TestSet(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender, _user_cmd)
        self.mocker.replay()

    def tearDown(self):
        User(_user_sender).deleteVariable(_var)

    def testSetCmd(self):
        Command.dispatch(self.user_msg)
        user = User(_user_sender)
        val = user.getVariable(_var)
        self.assertEqual(val, _val)

class TestIncompleteSet(MockerTestCase):

    def setUp(self):
        self.user_msg = _buildMsg(self.mocker, _user_sender, _incomplete_user_cmd)
        self.mocker.replay()

    def tearDown(self):
        User(_user_sender).deleteVariable(_var)

    def testSetCmd(self):
        Command.dispatch(self.user_msg)
        user = User(_user_sender)
        val = user.getVariable(_var)
        self.assertEqual(val, None)

class TestAdminSet(MockerTestCase):

    def setUp(self):
        self.admin_msg = _buildMsg(self.mocker, _admin_sender, _admin_cmd)
        self.mocker.replay()

    def tearDown(self):
        User(_admin_sender).deleteAdminVariable(_var)

    def testSetCmd(self):
        user = User(_admin_sender)
        user.makeAdmin()
        Command.dispatch(self.admin_msg)
        self.assertEqual(user.getAdminVariable(_var), _val)

class TestNonAdminSet(MockerTestCase):

    def setUp(self):
        self.admin_msg = _buildMsg(self.mocker, _user_sender, _admin_cmd)
        self.mocker.replay()
        self.var = AdminVariable(_var)

    def tearDown(self):
        self.var.delete()

    def testSetCmd(self):
        Command.dispatch(self.admin_msg)
        self.assertEqual(self.var.get(), None)

    def testSetCmdAgain(self):
        Command.dispatch(self.admin_msg)
        self.assertEqual(User(_user_sender).getAdminVariable(_var), None)
