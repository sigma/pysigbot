from mocker import MockerTestCase, ANY

from bot.commands import Command
from bot.users import User

_user_sender = "john.doe@example.com"
_cmd_1 = "rtm tasks list"
_cmd_2 = "rtm lists list"

class TestRtm(MockerTestCase):

    def _expect(self, expr):
        return self.expect(expr).count(0,None)

    def _buildMsg(self, sender, cmd):
        fake_msg = self.mocker.mock()

        self._expect(fake_msg.sender).result(sender)
        self._expect(fake_msg.body).result(cmd)
        self._expect(fake_msg.reply(ANY))

        return fake_msg

    def setUp(self):
        task = self.mocker.mock()
        self._expect(task.id).result("456789")
        tasks_list = self.mocker.mock()
        self._expect(tasks_list.tasks.list).result([task])

        list = self.mocker.mock()
        self._expect(list.id).result("123456")
        self._expect(list.name).result("plop")
        lists_list = self.mocker.mock()
        self._expect(lists_list.lists.list).result([list])

        rtm = self.mocker.mock()
        self._expect(rtm.tasks.getList()).result(tasks_list)
        self._expect(rtm.lists.getList()).result(lists_list)

        cls = self.mocker.replace("rtmlib.Rtm")
        self._expect(cls(None, None, None)).nospec().result(rtm)

        self.msg = [self._buildMsg(_user_sender, _cmd_1),
                    self._buildMsg(_user_sender, _cmd_2)]

        self.mocker.replay()

    def testTasksList(self):
        user_msg = self.msg[0]
        Command.dispatch(user_msg)

    def testListsList(self):
        user_msg = self.msg[1]
        Command.dispatch(user_msg)

TestRtm.status = "unstable"
TestRtm.component = "plugins"
TestRtm.plugin = "rtm"
