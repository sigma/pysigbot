from bot.commands import PrefixCommand
from google.appengine.api import memcache

from common.models import AdminVariable

from rtmlib import Rtm
import logging

class RtmRepository(object):

    @staticmethod
    def getUserRtm(user):
        rtmkey = "rtm.%s" % (user)
        try:
            rtm = memcache.get(rtmkey)
        except: # pragma nocover
            rtm = None

        if rtm is None:
            api = AdminVariable("rtm.api").get()
            secret = AdminVariable("rtm.secret").get()
            token = user.getVariable("rtm.token")
            rtm = Rtm(api, secret, token)
            try:
                if not memcache.add(rtmkey, rtm, 36000): # pragma nocover
                    logging.error("Memcache set failed.")
            except:
                pass
        return rtm

class RtmCmd(PrefixCommand):

    PREFIX = 'rtm'

class RtmTasksCmd(RtmCmd):

    PREFIX = 'tasks'

class RtmTasksListCmd(RtmTasksCmd):

    PREFIX = 'list'

    def run(self):
        rtm = RtmRepository.getUserRtm(self.sender)
        l = rtm.tasks.getList()
        return ",".join([t.id for t in l.tasks.list])

class RtmListsCmd(RtmCmd):

    PREFIX = 'lists'

class RtmListsListCmd(RtmListsCmd):

    PREFIX = 'list'

    def run(self):
        rtm = RtmRepository.getUserRtm(self.sender)
        l = rtm.lists.getList()
        return ["%08x: %s" % (int(l.id), l.name) for l in l.lists.list]
