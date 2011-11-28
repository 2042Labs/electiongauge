from django.core.exceptions import ValidationError
from django.db import models

# TODO: Figure out why relative import is not working properly?
#from .choices import FEED_TYPES
from egauge.apps.core.choices import FEED_TYPES

from .elections import Candidate

class Feed(models.Model):
    '''This is the model for feeds.'''

    feed_title = models.CharField(max_length=250, help_text='What do we call this feed for our purposes?')
    feed_url = models.URLField()
    feed_type = models.CharField(max_length=1, choices=FEED_TYPES)

    related_candidate = models.ForeignKey(Candidate, blank=True, null=True, help_text="If candidate, then which one?")
    related_topic = models.CharField(max_length=150, blank=True, help_text="If a topic, then which one?")

    def __unicode__(self):
        return self.feed_title

    def clean(self):
        if self.related_topic and self.related_candidate:
            raise ValidationError('You can only have a related candidate OR related topic. You can not have both.')
        else:
            if not self.related_topic:
                if not self.related_candidate:
                    raise ValidationError('You must have either a related topic or a related candiate.')

    def save(self):
        self.clean()


class Stem(models.Model):
    ''' Model that records stems.'''

    stem = models.CharField(max_length=250)

    def __unicode__(self):
        return self.stem


class ProcessedTweet(models.Model):
    ''' This is a model for processed tweets. '''

    unique_tweet_id = models.IntegerField(help_text='Unique tweet labeled as "id".')
    unique_tweet_id_str = models.CharField(max_length=250, help_text='Unique tweet id string labeled as "id_str".')

    date = models.DateTimeField(help_text='Date of tweet')

    raw_location = models.CharField(max_length=250, help_text='Location field of Tweet.')

    exact_lat_long = models.BooleanField(default=False, help_text='Is the lat & long exact?')
    latitude = models.IntegerField(help_text='', null=True, blank=True)
    longitude = models.IntegerField(help_text='', null=True, blank=True)

    #TODO: Match and save against normalized data tables
    city    = models.CharField(max_length=150, blank=True)
    county  = models.CharField(max_length=150, blank=True)
    state   = models.CharField(max_length=2, blank=True)
    country = models.CharField(max_length=150, blank=True)

    associated_feed = models.ForeignKey(Feed, help_text='Feed that pulled this tweet.')
    stems = models.ManyToManyField(Stem, help_text='Associated stems to this tweet.')

    def __unicode__(self):
        return self.unique_tweet_id, self.date, self.raw_location
