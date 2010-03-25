from mocker import MockerTestCase

from bot.commands import Command
from bot.users import User

_sender = "john.doe@example.com"
_cmd = "foo"

def _buildMsg(mocker):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(_sender)
    mocker.count(0, None)

    fake_msg.body
    mocker.result(_cmd)
    mocker.count(0, None)

    fake_msg.reply(Command.COMMAND_NOT_FOUND_MSG)

    return fake_msg

class TestUserNoCmd(MockerTestCase):

    def setUp(self):
        self.msg = _buildMsg(self.mocker)
        self.mocker.replay()

    def testNoCmd(self):
        Command.dispatch(self.msg)

TestUserNoCmd.status = "stable"
TestUserNoCmd.component = "cmd"
