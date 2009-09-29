import urllib
from md5 import md5

from api import API
import simplejson as json

SERVICE_URL = 'http://api.rememberthemilk.com/services/rest/'
AUTH_SERVICE_URL = 'http://www.rememberthemilk.com/services/auth/'

class RtmError(Exception): pass

class RtmApiError(RtmError): pass

class Rtm():

    def __init__(self, apiKey, secret, token, validator=None):
        self.apiKey = apiKey
        self.secret = secret
        self.token = token

        self.validationFunction = validator

        # this enables one to do 'rtm.tasks.getList()', for example
        for prefix, attributes in API.items():
            setattr(self, prefix,
                    RtmApiCategory(self, "rtm." + prefix, attributes))

    def _sign(self, params):
        "Sign the parameters with MD5 hash"
        pairs = ''.join(['%s%s' % (k,v) for k,v in self._sortedItems(params)])
        return md5(self.secret+pairs).hexdigest()

    def _sortedItems(self, dictionary):
        "Return a list of (key, value) sorted based on keys"
        keys = dictionary.keys()
        keys.sort()
        for key in keys:
            yield key, dictionary[key]

    def _openURL(self, url, queryArgs=None):
        if queryArgs:
            url = url + '?' + urllib.urlencode(queryArgs)
        return urllib.urlopen(url).read()

    def readJson(self, txt):
        data = DottedDict('ROOT', json.loads(txt))
        rsp = data.rsp

        if rsp.stat == 'fail':
            raise RtmApiError, 'API call failed - %s (%s)' % (
                rsp.err.msg, rsp.err.code)
        else:
            return rsp

    def handleApiError(self, f):
        f.trap(RtmApiError)

    def get(self, **params):
        "Get the XML response for the passed `params`."
        params['api_key'] = self.apiKey
        params['format'] = 'json'
        params['api_sig'] = self._sign(params)

        return self.readJson(self._openURL(SERVICE_URL, params))

class RtmApiCategory:
    "See the `API` structure and `RTM.__init__`"

    def __init__(self, rtm, prefix, attributes):
        self.rtm = rtm
        self.prefix = prefix

        for name in attributes.keys():
            definition = attributes[name]
            if type(definition) is dict:
                setattr(self, name, RtmApiCategory(self.rtm, self.prefix + '.' + name, definition))
            else:
                aname = '%s.%s' % (self.prefix, name)
                rargs, oargs = definition
                func = self.makeMethod(aname, rargs, oargs)
                setattr(self, name, func)

    def makeMethod(self, name, required, optional):
        return lambda **params: self.callMethod(name, required, optional, **params)

    def callMethod(self, aname, rargs, oargs, **params):
        # Sanity checks
        for requiredArg in rargs:
            if requiredArg not in params:
                raise TypeError, 'Required parameter (%s) missing' % requiredArg

        for param in params:
            if param not in rargs + oargs:
                warnings.warn('Invalid parameter (%s)' % param)

        return self.rtm.get(method=aname,
                            auth_token=self.rtm.token,
                            **params)

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

    def __repr__(self):
        children = [c for c in dir(self) if not c.startswith('_')]
        return 'dotted <%s> : %s' % (
            self._name,
            ', '.join(children))
