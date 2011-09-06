import datetime
import traceback
import tweepy
import logging
import time
from functools import wraps
import inspect
from tweepy.error import TweepError

LOG = logging.getLogger('twitter')

__author__ = 'Alex'

query = {
    'q': '"american express" OR "american xpress" OR "americanexpress com" OR "amx" OR "my card can" OR "amex.com" OR "amex" OR "amex rewards" OR "jetblue"',
    #'since': '2011-01-10',
    'lang': 'en',
    'rpp': 90,
}

_API = None # connect once
current_creds = None

def get_auth():
    from analyticsapp.models import TwitterCredentials
    now = datetime.datetime.now()
    auth = None
    creds = TwitterCredentials.objects.filter(active=True).order_by('last_rate_exceeded')
    while not auth:
        for cred in creds:
            if cred.last_rate_exceeded:
                ago = now - cred.last_rate_exceeded
                LOG.info("Checking credentials %s: %s" % (cred.pk, ago))
                # Ignore if rate exceeded less than 10 minutes ago
                if ago < datetime.timedelta(minutes=10):
                    continue
            global current_creds
            current_creds = cred
            auth = mk_auth(cred)
        if auth:
            current_creds.last_used = datetime.datetime.now()
            current_creds.save()
            print "Using credentials %s" % current_creds.pk
            return auth

        sleepminutes = 15
        LOG.error("No credentials available, sleeping for %s" % sleepminutes)
        time.sleep(sleepminutes * 60)

def mk_auth(twitter_credentials):
    ret = tweepy.OAuthHandler(twitter_credentials.oauth_token, twitter_credentials.oauth_secret)
    ret.set_access_token(twitter_credentials.access_key, twitter_credentials.access_secret)
    return ret

def timeout_wrapper(func):
    @wraps(func)
    def timeout(*args, **kwargs):
        # Rate limit checking proxy
        result = None
        success = False
        response_code = 0
        while not success:
            try:
                result = func(*args, **kwargs)
                success = True
                rate_status = connect().rate_limit_status()
            except TweepError,e:
                print e
                if e.response:
                    response_code = e.response.status
                    if response_code in [503, 502, 500]:
                        LOG.info("Caught code %s, sleeping for 10" % response_code)
                        time.sleep(10)
                    if response_code != 420:
                        raise
                else:
                    raise
            if response_code == 420 or (rate_status and rate_status['remaining_hits'] < 10):
                LOG.info('Rate limit reached, rotating credentials')
                global current_creds
                current_creds.last_rate_exceeded = datetime.datetime.now()
                current_creds.save()

                _API.auth = get_auth()
        return result
    return timeout

def connect(reuse=True):
    global _API
    if reuse and _API: return _API
    auth = get_auth()

#    if not auth:
#        auth = tweepy.OAuthHandler("oJemkCmfInHa1MiABezvfw", "dARJ3HcyU3w8EaHy5lH1klA2WKsd1djXVo1qnIFJg")
#        auth.set_access_token("169938890-HPn5jkMHi8z4CZKRWt0yYshqcGMyXbdXSYStPXQx", "piqhegGJg8F5yKmraKYsXAJCmacZtyAnFhAdJhvwp90")
    api = tweepy.API(auth)
    if not api:
        LOG.error("Tweepy could not connect...")
    try:
        # This counts as one request.
        cred = api.verify_credentials()
        if cred:
            LOG.info("Twitter login successful (%s)" % str(cred.__dict__))
            _API = api
        else:
            LOG.error("Twitter login failed (%s)" % str(cred))
            current_creds.last_rate_exceeded = datetime.datetime.now()
            current_creds.save()
            return None
    except:
        LOG.error("Error while logging in: %s" % str(auth))
        traceback.print_exc()
        return None

    # A little black magic to make calls sleep if rate limit is near.
    if api:
        for name, func in inspect.getmembers(api):
            if inspect.ismethod(func) and name not in ['rate_limit_status']:
                setattr(api, name, timeout_wrapper(func))
    return api

def run_query(api = None, query = query):
    if not api:
        api = connect()
    # Expecting twitter api from connect() and neo4j graph db from db.connect()
    tweets = api.search(**query)
    return tweets
