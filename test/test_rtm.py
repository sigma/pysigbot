from mocker import MockerTestCase

from rtmlib.rtm import Rtm

class TestRtmSanity(MockerTestCase):

    def setUp(self):
        self.rtm = Rtm(apiKey="dummy key",
                       secret="dummy secret",
                       token="dummy token")

    def testAccessors(self):
        self.assertTrue(callable(self.rtm.lists.delete))
        self.assertTrue(callable(self.rtm.auth.getToken))
        self.assertFalse(callable(self.rtm.tasks.notes))

TestRtmSanity.status = "unstable"
TestRtmSanity.component = "lib"
TestRtmSanity.lib = "rtm"
