from urllib import urlopen, urlencode
from md5 import md5

from api import API
import django.utils.simplejson as json

SERVICE_URL = 'http://api.rememberthemilk.com/services/rest/'
AUTH_SERVICE_URL = 'http://www.rememberthemilk.com/services/auth/'

class RtmError(Exception): pass

class RtmApiError(RtmError): pass

class ApiNode(object):

    def __init__(self, fqn, definition):
        self.__fqn = fqn
        self.__def = definition
        self.__callable = False
        self.__req_args = None
        self.__opt_args = None
        if isinstance(self.__def, dict):
            # category object
            for key, value in self.__def.items():
                self.__dict__[key] = ApiNode("%s.%s" % (self.__fqn, key), value)
        else:
            # method object
            self.__callable = True
            self.__req_args, self.__opt_args = self.__def

    def __call__(self, rtm, **kwargs):
        if self.__callable:
            for a in self.__req_args: # pragma nocover
                if a not in kwargs:
                    raise TypeError, 'Required parameter (%s) missing' % (a)

            for a in kwargs: # pragma nocover
                if a not in self.__req_args + self.__opt_args:
                    warnings.warn('Invalid parameter (%s)' % (param))

            return rtm._get(method=self.__fqn,
                            auth_token=rtm._token,
                            **kwargs)
        else: # pragma nocover
            raise TypeError, "%s is not a method !" % (self.__fqn)

class ApiCtxt(object):

    def __init__(self, rtm, node):
        self.__rtm = rtm
        self.__node = node

    def __getattr__(self, attr):
        node = getattr(self.__node, attr)
        return ApiCtxt(self.__rtm, node)

    def __call__(self, **kwargs):
        return self.__node(self.__rtm, **kwargs)

_rtm_node = ApiNode('rtm', API)

class RtmTransport(object):

    def __init__(self):
        pass

    def get(self, params):
        return self._readJson(self._openURL(SERVICE_URL, params))

    # this will be mocked
    def _urlopen(self, url): # pragma nocover
        return urlopen(url).read()

    def _openURL(self, url, queryArgs=None):
        if queryArgs:
            url = url + '?' + urlencode(queryArgs)
        return self._urlopen(url)

    def _readJson(self, txt):
        data = DottedDict('ROOT', json.loads(txt))
        rsp = data.rsp

        if rsp.stat == 'fail':
            raise RtmApiError, 'API call failed - %s (%s)' % (
                rsp.err.msg, rsp.err.code)
        else:
            return rsp

class Rtm():

    def __init__(self, apiKey, secret, token):
        self._apiKey = apiKey
        self._secret = secret
        self._token = token
        self._transport = RtmTransport()
        self.__rtm = ApiCtxt(self, _rtm_node)

    def __getattr__(self, attr):
        return getattr(self.__rtm, attr)

    def _sign(self, params):
        "Sign the parameters with MD5 hash"
        pairs = ''.join(['%s%s' % (k,v) for k,v in self._sortedItems(params)])
        return md5(self._secret+pairs).hexdigest()

    def _sortedItems(self, dictionary):
        "Return a list of (key, value) sorted based on keys"
        keys = dictionary.keys()
        keys.sort()
        for key in keys:
            yield key, dictionary[key]

    def _get(self, **params):
        "Get the XML response for the passed `params`."
        params['api_key'] = self._apiKey
        params['format'] = 'json'
        params['api_sig'] = self._sign(params)

        return self._transport.get(params)

class DottedDict(object):
    "Make dictionary items accessible via the object-dot notation."

    def __init__(self, name, dictionary):
        self._name = name

        if type(dictionary) is dict:
            for key, value in dictionary.items():
                if type(value) is dict:
                    value = DottedDict(key, value)
                elif type(value) in (list, tuple) and key != 'tag':
                    value = [DottedDict('%s_%d' % (key, i), item)
                             for i, item in self._indexed(value)]
                setattr(self, key, value)

    def _indexed(self, seq):
        index = 0
        for item in seq:
            yield index, item
            index += 1

    def __repr__(self): # pragma nocover
        children = [c for c in dir(self) if not c.startswith('_')]
        return 'dotted <%s> : %s' % (self._name, ', '.join(children))
