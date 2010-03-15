from mocker import MockerTestCase, ANY

from bot.commands import Command
from bot.users import User

_sender = "john.doe@example.com"
_var = "plop"
_val = "foo"
_cmd = "set %s %s" % (_var, _val)

class TestUser(MockerTestCase):

    def setUp(self):
        fake_msg = self.mocker.mock()

        fake_msg.sender
        self.mocker.result(_sender)
        self.mocker.count(0, None)
        fake_msg.body
        self.mocker.result(_cmd)
        fake_msg.reply(ANY)
        self.mocker.replay()
        self.fake_msg = fake_msg

    def testSetCmd(self):
        Command.dispatch(self.fake_msg)
        user = User(_sender)
        val = user.getVariable(_var)
        self.assertEqual(val, _val)
