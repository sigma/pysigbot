from mocker import MockerTestCase, ANY

from bot.commands import Command
from bot.users import User

_user_sender = "john.doe@example.com"
_cmd_1 = "rtm tasks list"
_cmd_2 = "rtm lists list"

def _buildMsg(mocker, sender, cmd):
    fake_msg = mocker.mock()

    fake_msg.sender
    mocker.result(sender)
    mocker.count(0, None)

    fake_msg.body
    mocker.result(cmd)
    mocker.count(0, None)

    fake_msg.reply(ANY)

    return fake_msg

class TestRtm(MockerTestCase):

    def setUp(self):
        pass

    def testTasksList(self):
        user_msg = _buildMsg(self.mocker, _user_sender, _cmd_1)

        t = self.mocker.mock()
        self.expect(t.id).result("foobar")

        l = self.mocker.mock()
        self.expect(l.tasks.list).result([t])

        rtm = self.mocker.mock()
        self.expect(rtm.tasks.getList()).result(l)

        cls = self.mocker.replace("rtmlib.Rtm")
        self.expect(cls(None, None, None)).nospec().result(rtm)

        self.mocker.replay()

        Command.dispatch(user_msg)

    def testListsList(self):
        user_msg = _buildMsg(self.mocker, _user_sender, _cmd_2)

        t = self.mocker.mock()
        self.expect(t.id).result(123456)
        self.expect(t.name).result("plop")

        l = self.mocker.mock()
        self.expect(l.lists.list).result([t])

        rtm = self.mocker.mock()
        self.expect(rtm.lists.getList()).result(l)

        cls = self.mocker.replace("rtmlib.Rtm")
        self.expect(cls(None, None, None)).nospec().result(rtm)

        self.mocker.replay()

        Command.dispatch(user_msg)


TestRtm.status = "unstable"
TestRtm.component = "plugins"
TestRtm.plugin = "rtm"
