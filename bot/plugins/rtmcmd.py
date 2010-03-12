from bot.commands import PrefixCommand
from google.appengine.api import memcache
from google.appengine.ext import db
from rtmlib import Rtm
import logging

class RtmRepository(object):

    @staticmethod
    def getUserRtm(user):
        rtmkey = "rtm.%s" % (user)
        try:
            rtm = memcache.get(rtmkey)
        except:
            rtm = None

        if rtm is None:
            api = db.GqlQuery("SELECT * FROM DbAdminVariable WHERE name = :1", "rtm.api").get().value
            secret = db.GqlQuery("SELECT * FROM DbAdminVariable WHERE name = :1", "rtm.secret").get().value
            token = db.GqlQuery("SELECT * FROM DbUserVariable WHERE name = :1", "%s/rtm.token" % (user)).get().value
            rtm = Rtm(api, secret, token)
            try:
                if not memcache.add(rtmkey, rtm, 36000):
                    logging.error("Memcache set failed.")
            except:
                pass
        return rtm

class RtmCmd(PrefixCommand):

    PREFIX = 'rtm'

    def run(self):
        return "rtm " + self.args[0]

class RtmTasksCmd(RtmCmd):

    PREFIX = 'tasks'

    def run(self):
        return "rtm.tasks " + self.args[0]

class RtmTasksListCmd(RtmTasksCmd):

    PREFIX = 'list'

    def run(self):
        rtm = RtmRepository.getUserRtm(self.sender)
        l = rtm.tasks.getList()
        return ",".join([t.id for t in l.tasks.list])

class RtmListsCmd(RtmCmd):

    PREFIX = 'lists'

    def run(self):
        return "rtm.lists " + self.args[0]

class RtmListsListCmd(RtmListsCmd):

    PREFIX = 'list'

    def run(self):
        rtm = RtmRepository.getUserRtm(self.sender)
        l = rtm.lists.getList()
        return ["%08x: %s" % (int(l.id), l.name) for l in l.lists.list]
