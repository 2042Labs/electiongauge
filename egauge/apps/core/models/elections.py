from django.db import models
from ..choices import ELECTION_TYPES


class OfficeType(models.Model):
    '''Office types are Senator/Rep/Governor, etc'''

    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'core'

class Office(models.Model):

    office_name = models.CharField(max_length=75)
    office_type = models.ForeignKey(OfficeType)
    #location    = models.ForeignKey(Location)

    def __unicode__(self):
        return self.office_name

    class Meta:
        app_label = 'core'

class Party(models.Model):

    abbrev   = models.CharField(max_length=2, unique=True)
    name     = models.CharField(max_length=50)

    def __unicode__(self):
        return self.party

    class Meta:
        app_label = 'core'

# TODO: QUESTION: Can we get this info from somewhere & auto magically populate, so we don't have to maintain.
class Election(models.Model):
    '''an election at the state or national level; associated with Candidates'''

    display_name = models.CharField(max_length=250, help_text='name of the election for general reference on front-end')
    election_type = models.CharField(max_length=1, choices=ELECTION_TYPES)
    upcoming_election = models.ForeignKey('self', null=True, blank=True, related_name='primaries_set')
    #TODO: Add location back to election
    #location = models.ForeignKey(Location, help_text='the jurisdiction of the election')
    office = models.ForeignKey(Office, help_text='Senate, Governor, President')
    party = models.ForeignKey(Party, null=True, blank=True, help_text="only for primaries")
    polling_date = models.DateField()

    def __unicode__(self):
        return self.display_name

    class Meta:
        app_label = 'core'

# a candidate participating in at least one election
class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    party = models.CharField(max_length=30) # 'republican', 'green', 'know-nothing'
    website = models.URLField() # more info!
    election = models.ForeignKey(Election, blank=True, null=True, help_text='Election in which the candidate is running.') # the election in which Candidate is running (ONLY ONE ELECTION PER CANDIDATE)

    photo = models.URLField()
    photo_height = models.IntegerField(blank=True, null=True)
    photo_weight = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        app_label = 'core'