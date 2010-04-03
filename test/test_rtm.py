from mocker import MockerTestCase, ANY
from urllib import urlencode

from rtmlib.rtm import Rtm, SERVICE_URL, DottedDict, RtmApiError

API_KEY = "dummy key"
SECRET  = "dummy secret"
TOKEN   = "dummy token"

SAMPLE_REQUEST = (SERVICE_URL + '?' +
                  urlencode({'api_sig': '27d94386de9f6b9fc9901549b50a5ef8',
                             'auth_token': 'dummy token',
                             'api_key': 'dummy key',
                             'method': 'rtm.tasks.getList',
                             'format': 'json'}))

SAMPLE_RESPONSE = """{"rsp":
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
                                        "estimate":""}}]}]}}}"""

SAMPLE_ERROR = """{"rsp":
     {"stat":"fail",
      "err":{
          "msg":"sample error",
          "code":"123"}}}"""

class TestRtmSanity(MockerTestCase):

    def setUp(self):
        self.rtm = Rtm(apiKey=API_KEY,
                       secret=SECRET,
                       token=TOKEN)

    def testAccessors(self):
        self.assertTrue(callable(self.rtm.lists.delete))
        self.assertTrue(callable(self.rtm.auth.getToken))

    def testTasksGetList(self):
        obj = self.mocker.patch(self.rtm._transport)

        obj._urlopen(SAMPLE_REQUEST)
        self.mocker.result(SAMPLE_RESPONSE)
        self.mocker.replay()

        resp = self.rtm.tasks.getList()
        self.assertTrue(isinstance(resp, DottedDict))
        self.assertTrue(resp.stat == "ok")

    def testTasksGetListError(self):
        obj = self.mocker.patch(self.rtm._transport)

        obj._urlopen(SAMPLE_REQUEST)
        self.mocker.result(SAMPLE_ERROR)
        self.mocker.replay()

        self.assertRaises(RtmApiError, self.rtm.tasks.getList)

TestRtmSanity.status = "unstable"
TestRtmSanity.component = "lib"
TestRtmSanity.lib = "rtm"
