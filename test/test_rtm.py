from mocker import MockerTestCase, ANY

from rtmlib.rtm import Rtm, SERVICE_URL, DottedDict

class TestRtmSanity(MockerTestCase):

    def setUp(self):
        self.rtm = Rtm(apiKey="dummy key",
                       secret="dummy secret",
                       token="dummy token")

    def testAccessors(self):
        self.assertTrue(callable(self.rtm.lists.delete))
        self.assertTrue(callable(self.rtm.auth.getToken))

    def testTasksGetList(self):
        obj = self.mocker.patch(self.rtm._transport)

        obj._openURL(SERVICE_URL,
                {'api_sig': '27d94386de9f6b9fc9901549b50a5ef8',
                 'auth_token': 'dummy token',
                 'api_key': 'dummy key',
                 'method': 'rtm.tasks.getList',
                 'format': 'json'})
        self.mocker.result("""{"rsp":
     {"stat":"ok",
      "tasks":{
            "rev":"gw4ycm4ios8wg4480ck8kcskgwksc4k",
            "list":[
                {"id":"987654321"},
                {"id":"123456789",
                 "taskseries":[{"id":"123456789",
                                "created":"2006-05-07T10:19:54Z",
                                "modified":"2006-05-07T10:19:54Z",
                                "name":"Get Bananas",
                                "source":"api",
                                "url":"",
                                "location_id":"",
                                "tags":{"tag":["foo","bar"]},
                                "participants":[],
                                "notes":[],
                                "task":{"id":"987654321",
                                        "due":"",
                                        "has_due_time":"0",
                                        "added":"2006-05-07T10:19:54Z",
                                        "completed":"",
                                        "deleted":"",
                                        "priority":"N",
                                        "postponed":"0",
                                        "estimate":""}}]}]}}}""")
        self.mocker.replay()

        resp = self.rtm.tasks.getList()
        self.assertTrue(isinstance(resp, DottedDict))
        self.assertTrue(resp.stat == "ok")

TestRtmSanity.status = "unstable"
TestRtmSanity.component = "lib"
TestRtmSanity.lib = "rtm"
