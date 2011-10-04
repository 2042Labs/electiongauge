from django.db import models

from egauge.core import choices
from egauge.geo_data.models import * #TODO: make sure file models explicits lists models. This is sloppy.



POLITICAL_OFFICES = (
    ('','')
)


class ExternalURLS(models.Model):
    url = models.URLField()
    linked_text = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True




# a tag associated with at least one of the tweets collected
class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)



class Location(models.Model):

    city    = models.ForeignKey(City, null=True, blank=True)
    county  = models.ForeignKey(County, null=True, blank=True)
    state   = models.ForeignKey(State, null=True, blank=True)
    country = models.ForeignKey(Country)


class OfficeType(models.Model):
    '''Office types are Senator/Rep/Governor, etc'''

    name = models.CharField(max_length=50)
    slug = models.SlugField()


class Office(models.Model):

    office_name = models.CharField(max_length=75)
    office_type = models.ForeignKey(OfficeType)
    location    = models.ForeignKey(Location)

# QUESTION: Can we get this info from somewhere & auto magically populate, so we don't have to maintain.
class Election(models.Model):
    '''an election at the state or national level; associated with Candidates'''

    display_name = models.CharField(max_length=250, help_text='name of the election for general reference on front-end')
    election_type = models.CharField(max_length=1, choices=choices.ELECTION_TYPES)
    upcoming_election = models.ForeignKey('self', null=True, blank=True, related_name='primaries_set')
    location = models.ForeignKey(Location, help='the jurisdiction of the election')
    office = models.ForeignKey(Office, help_text='Senate, Governor, President')
    party = models.ForeignKey(Party, null=True, blank=True, help_text="only for primaries")
    polling_date = models.DateField()


# a candidate participating in at least one election
class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    party = models.CharField(max_length=30) # 'republican', 'green', 'know-nothing'
    website = models.URLField() # more info!
    election = models.ForeignKey(Election) # the election in which Candidate is running (ONLY ONE ELECTION PER CANDIDATE)

    photo = models.URLField()
    photo_height = models.IntegerField(blank=True, null=True)
    photo_weight = models.IntegerField(blank=True, null=True)

# a processed tweet taken from Twitter and parsed for information about the
# candidates and elections it references as well as its origin point. The text
# of the original message is retained
class Tweet(models.Model):
    text = models.CharField(max_length=200) # however long tweets are?
    candidates = models.ManyToManyField(Candidate) # who does it reference
    elections = models.ManyToManyField(Election) # which election does it reference
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=10, decimal_places=8)
