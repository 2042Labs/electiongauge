import time
from getpass import getpass
from textwrap import TextWrapper
import json
import sys

import tweepy

import pymongo as mongo

"""
Tweets come into : StreamWatcherListener.on_status
 
Status object structure:
{
 'contributors': None,
 'truncated': False,
 'text': 'My Top Followers in 2010: @tkang1 @serin23 @uhrunland @aliassculptor @kor0307 @yunki62. Find yours @ http://mytopfollowersin2010.com',
 'in_reply_to_status_id': None,
 'id': 21041793667694593,
 '_api': <tweepy.api.api object="" at="" 0x6bebc50="">,
 'author': <tweepy.models.user object="" at="" 0x6c16610="">,
 'retweeted': False,
 'coordinates': None,
 'source': 'My Top Followers in 2010',
 'in_reply_to_screen_name': None,
 'id_str': '21041793667694593',
 'retweet_count': 0,
 'in_reply_to_user_id': None,
 'favorited': False,
 'retweeted_status': <tweepy.models.status object="" at="" 0xb2b5190="">,
 'source_url': 'http://mytopfollowersin2010.com',
 'user': <tweepy.models.user object="" at="" 0x6c16610="">,
 'geo': None,
 'in_reply_to_user_id_str': None,
 'created_at': datetime.datetime(2011, 1, 1, 3, 15, 29),
 'in_reply_to_status_id_str': None,
 'place': None
}


User Object:
{
 'follow_request_sent': False,
 'profile_use_background_image': True,
 'id': 132728535,
 '_api': <tweepy.api.api object="" at="" xxxxxxx="">,
 'verified': False,
 'profile_sidebar_fill_color': 'C0DFEC',
 'profile_text_color': '333333',
 'followers_count': 80,
 'protected': False,
 'location': 'Seoul Korea',
 'profile_background_color': '022330',
 'id_str': '132728535',
 'utc_offset': 32400,
 'statuses_count': 742,
 'description': "Cars, Musics, Games, Electronics, toys, food, etc... I'm just a typical boy!",
 'friends_count': 133,
 'profile_link_color': '0084B4',
 'profile_image_url': 'http://a1.twimg.com/profile_images/1213351752/_2_2__normal.jpg',
 'notifications': False,
 'show_all_inline_media': False,
 'geo_enabled': True,
 'profile_background_image_url': 'http://a2.twimg.com/a/1294785484/images/themes/theme15/bg.png',
 'screen_name': 'jaeeeee',
 'lang': 'en',
 'following': True,
 'profile_background_tile': False,
 'favourites_count': 2,
 'name': 'Jae Jung Chung',
 'url': 'http://www.carbonize.co.kr',
 'created_at': datetime.datetime(2010, 4, 14, 1, 20, 45),
 'contributors_enabled': False,
 'time_zone': 'Seoul',
 'profile_sidebar_border_color': 'a8c7f7',
 'is_translator': False,
 'listed_count': 2
}

"""



class StreamWatcherListener(tweepy.StreamListener):

    status_wrapper = TextWrapper(width=60, initial_indent=' ', subsequent_indent=' ')

    def on_status(self, status):
        try:
            print self.status_wrapper.fill(status.text)
            print '\n %s %s via %s\n' % (status.author.screen_name, status.created_at, status.source)
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'



class MongoStreamer(StreamWatcherListener):

    def __init__(self, *args, **kwargs):
        super(MongoStreamer, self).__init__(*args, **kwargs)
        ## initialize the Mongo connection
        self.connection = mongo.Connection()
        self.db = self.connection.twitter
        self.tweets = self.db.tweets
        self.tweets.create_index([("date", mongo.DESCENDING), ("author", mongo.ASCENDING)])
        
    def tweepy2json(self,status):
        out={}
        user=status.author
        out['author']=user.screen_name
        out['followers']=user.followers_count
        out['profile']=user.description
        out['text']=status.text
        out['date']=str(status.created_at)
        out['loc']=user.location
        out['geo']=str(status.geo)
        out['place']=str(status.place)
        
        return(out)


    def on_status(self, status):
        try:
            json=self.tweepy2json(status)
            out=self.tweets.insert(json)
            print self.tweets.count()
        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            print "error:", sys.exc_info()[0]
            pass


def run():
    ##Twitter credentials
    username='ElectionGauge'
    password='cssgmu'
    stream = tweepy.Stream(username, password, MongoStreamer(), timeout=None)
    follow_list=[]#'obama,palin,romney'.split(',')
    keywords='obama,economy,recession,jobs,afghanistan'.split(',')
    stream.filter(follow_list, keywords)
    

def main():
    # Prompt for login credentials and setup stream object
    username = raw_input('Twitter username: ')
    password = getpass('Twitter password: ')
    stream = tweepy.Stream(username, password, StreamWatcherListener(), timeout=None)

    # Prompt for mode of streaming
    valid_modes = ['sample', 'filter']
    while True:
        mode = raw_input('Mode? [sample/filter] ')
        if mode in valid_modes:
            break
        print 'Invalid mode! Try again.'

    if mode == 'sample':
        stream.sample()

    elif mode == 'filter':
        follow_list = raw_input('Users to follow (comma separated): ').strip()
        track_list = raw_input('Keywords to track (comma seperated): ').strip()
        if follow_list:
            follow_list = [u for u in follow_list.split(',')]
        else:
            follow_list = None
        if track_list:
            track_list = [k for k in track_list.split(',')]
        else:
            track_list = None

        stream.filter(follow_list, track_list)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print '\nGoodbye!'