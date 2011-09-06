import datetime
import random
import urllib2
import dateutil.parser

__author__ = 'Alex'

def dictize(obj, filter=None):
    "Turns an object into dictionary. Filter is a function called on every (k,v) pair."
    ret = obj
    if type(obj) in [list, tuple]:
        return [dictize(o, filter) for o in obj]
    if getattr(obj, '__dict__', None):
        ret = dict()
        for (k,v) in obj.__dict__.iteritems():
            if not filter or (filter and filter(k,v)):
                ret[k] = dictize(v, filter)
    return ret

def mk_date(dic):
    "Turns tweet date dict into a date object."
    if isinstance(dic, datetime.datetime):
        return dic
    elif isinstance(dic, unicode):
        return dateutil.parser.parse(dic)
    else:
        args = [dic['_datetime__%s'%x] for x in ['year','month','day','hour','minute','second','microsecond']]
        return datetime.datetime(*args)

def encode(*args):
    '''Prepare string for DB insertion'''
    if len(args) > 1:
        return [encode(x) for x in args]
    string = args[0]
    if isinstance(string, str) or isinstance(string, unicode):
        return string.encode('utf-8')
    return string

url_cache = {}  # in-memory url cache
def deshorten(url):
    # Check cache (this could be a decorator)
    global url_cache
    if url in url_cache:
        return url_cache[url]
    surl = url

    resp = urllib2.urlopen(url, data=None, timeout=1)
    while resp.getcode() == 200 and url != resp.url:
        url = resp.url
        resp = urllib2.urlopen(url, data=None, timeout=1)
    if resp.getcode() != 200:
        raise Exception("Bad url: %s" % url.encode('ascii'))

    # Update cache
    if len(url_cache > 9000):
        # It's over 9000! Purge a random unlucky element, but prevent a memory leak.
        del url_cache[random.choice(url_cache.keys())]
    url_cache[surl] = url

    return url
