from django.core.exceptions import ValidationError
from django.db import models

from ..choices import FEED_TYPES
from .elections import Candidate

class TwitterTopic(models.Model):
    '''Model that holds Twitter topics.'''

    topic = models.CharField(max_length=250)

    def __unicode__(self):
        return self.topic

    class Meta:
        app_label = 'core'


class TweetFeed(models.Model):
    '''This is the model for canidate feeds.'''
    # Note, this was written to house topic & candidate feeds.
    # Code for topic feeds was comment out just in case we want to bring
    # it back later.

    feed_title = models.CharField(max_length=250, help_text='What do we call this feed for our purposes?')
    feed_url = models.URLField()
    #feed_type = models.CharField(max_length=1, default='C', choices=FEED_TYPES)

    related_candidate = models.ForeignKey(Candidate, blank=True, null=True, help_text="If candidate, then which one?")
    #related_topic = models.ForeignKey(TwitterTopic, blank=True, null=True, help_text="If a topic, then which one?")

    def __unicode__(self):
        return self.feed_title

    #def clean(self):
    #    if self.related_topic and self.related_candidate:
    #        raise ValidationError('You can only have a related candidate OR related topic. You can not have both.')
    #    else:
    #        if not self.related_topic:
    #            if not self.related_candidate:
    #                raise ValidationError('You must have either a related topic or a related candiate.')
    #
    #def save(self):
    #    self.clean()

    class Meta:
        app_label = 'core'


class WordStem(models.Model):
    ''' Model that records stems.'''

    stem = models.CharField(max_length=250)

    def __unicode__(self):
        return self.stem

    class Meta:
        app_label = 'core'

class TweetWordStemAndFreq(models.Model):
    ''' Model that records freq and stems.'''

    stem = models.ForeignKey(WordStem)
    frequency = models.IntegerField()

    def __unicode__(self):
        return self.stem, self.frequency

    class Meta:
        app_label = 'core'

class ProcessedTweet(models.Model):
    ''' This is a model for processed tweets. '''

    unique_tweet_id = models.IntegerField(help_text='Unique tweet labeled as "id".')
    unique_tweet_id_str = models.CharField(max_length=250, help_text='Unique tweet id string labeled as "id_str".')

    date = models.DateTimeField(help_text='Date of tweet')

    # Location information of tweet
    #{u'neighborhood': u'Hereford', u'house': u'', u'county': u'Baltimore County', u'street': u'', u'radius': 1400, u'quality': 50, u'unit': u'', u'city': u'Monkton', u'countrycode': u'US', u'woeid': 2420227, u'xstreet': u'', u'line4': u'United States', u'line3': u'', u'line2': u'Hereford, MD  21111', u'line1': u'', u'state': u'Maryland', u'latitude': u'39.590370', u'hash': u'', u'unittype': u'', u'offsetlat': u'39.590370', u'statecode': u'MD', u'postal': u'21111', u'name': u'', u'uzip': u'21111', u'country': u'United States', u'longitude': u'-76.663223', u'countycode': u'', u'offsetlon': u'-76.663223', u'woetype': 7}

    exact_lat_long = models.BooleanField(default=False, help_text='Is the lat & long exact?')

    latitude = models.IntegerField(help_text='', null=True, blank=True)
    longitude = models.IntegerField(help_text='', null=True, blank=True)
    city    = models.CharField(max_length=250, blank=True)
    county  = models.CharField(max_length=250, blank=True)
    state   = models.CharField(max_length=2, blank=True)

    associated_feed = models.ForeignKey(TweetFeed, help_text='Feed that pulled this tweet.')
    stems = models.ManyToManyField(TweetWordStemAndFreq, help_text='Associated stems and frequencies to this tweet.')

    def __unicode__(self):
        return "%s, %s, Latitude: %s, Longitude: %s" % self.unique_tweet_id, self.date, self.latitude, self.longitude

    class Meta:
        app_label = 'core'