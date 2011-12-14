from django.contrib import admin
from egauge.apps.core.models import OfficeType, Office, Party, Election, \
    Candidate, TwitterTopic, TweetFeed, WordStem, TweetWordStemAndFreq, \
    ProcessedTweet

# Election Related
class OfficeTypeAdmin(admin.ModelAdmin):
    pass

class OfficeAdmin(admin.ModelAdmin):
    pass

class PartyAdmin(admin.ModelAdmin):
    pass

class ElectionAdmin(admin.ModelAdmin):
    pass

class CandidateAdmin(admin.ModelAdmin):
    pass

# Tweet Related
class TwitterTopicAdmin(admin.ModelAdmin):
    pass

class TweetFeedAdmin(admin.ModelAdmin):
    pass

# Do we really need an email for this? I don't think so.
#class WordStemAdmin(admin.ModelAdmin):
#    pass

# Do we really need an email for this? I don't think so.
#class TweetWordStemAndFreqAdmin(admin.ModelAdmin):
#    pass

class ProcessedTweetAdmin(admin.ModelAdmin):
    pass

admin.site.register(OfficeType, OfficeTypeAdmin)
admin.site.register(Office, OfficeAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(TwitterTopic, TwitterTopicAdmin)
admin.site.register(TweetFeed, TweetFeedAdmin)
#admin.site.register(WordStem, WordStemAdmin)
#admin.site.register(TweetWordStemAndFreq, TweetWordStemAndFreqAdmin)
admin.site.register(ProcessedTweet, ProcessedTweetAdmin)




