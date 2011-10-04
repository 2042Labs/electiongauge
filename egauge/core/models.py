from django.db import models


# a tag associated with at least one of the tweets collected
class Tag(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

# an election at the state or national level; associated with Candidates
class Election(models.Model):
    position = models.CharField(max_length=30) # Senate, Governor, President
    location = models.CharField(max_length=30) # Virginia, Kentucky, USA

# a candidate participating in at least one election
class Candidate(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    party = models.CharField(max_length=30) # 'republican', 'green', 'know-nothing'
    photo = models.ImageField()
    website = models.URLField() # more info!
    election = models.ForeignKey(Election)
	# the election in which Candidate is running (ONLY ONE ELECTION PER CANDIDATE)



# a processed tweet taken from Twitter and parsed for information about the
# candidates and elections it references as well as its origin point. The text
# of the original message is retained
class Tweet(models.Model):
    text = models.CharField(max_length=200) # however long tweets are?
    candidates = models.ManyToManyField(Candidate) # who does it reference
    elections = models.ManyToManyField(Election) # which election does it reference
    latitude = models.DecimalField()
    longitude = models.DecimalField()
