from datetime import datetime, timedelta
import sys
import threading

__author__ = 'Alex'

import time
from textwrap import TextWrapper
import logging
import tweepy, simplejson
import getopt
import streamloader
from streamlistener import S3StoreListener, DbStreamListener, AggregateUFListener
from db_s3 import S3StreamUploader

__version__ = "$Revision: 1273 $".split()[1]

LOG = logging.getLogger('stream')

def usage():
    print '''Usage:
    -u username[,username,...]  Twitter username(s)
    -p password                 Twitter password
    --process                   process stream and save directly to db
    -c creator                  string to go into "created_by" field in tweet table
    --follow=user[,user,...]    Follow users (for filter stream)
    --track=keyword[,...]       Track keywords (for filter stream)
--process only options:
    --batch-size=<size>         size of tweet batch
    --no-db                     fake database operations (for testing streaming machinery)
    -v                          verbose'''

def start_streams(listener, password, streams, usernames, follow=(), track=()):
    for _user in usernames:
        print 'Connecting as %s/%s' % (_user, password)
        stream = tweepy.Stream(_user, password, listener, timeout=60)
        if follow or track:
            print "Starting filter on %s/%s" % (','.join(follow), ','.join(track))
            stream.filter(follow=follow, track=track, async=True)
        else:
            print "Starting sample"
            stream.sample(async=True)
        streams.append(stream)

def stop_streams(streams):
    for stream in streams:
        if stream.running:
            print "Closing stream."
            stream.running = False
    del streams[:]  # streams.clear()

def run():
    logging.basicConfig(level=logging.DEBUG,format="%(asctime)s %(name)s:%(levelname)s: %(message)s")
    logging.getLogger('neo4jrest').setLevel(logging.INFO)

    password = '!deepmile'
    usernames = list()
    use_files = False
    conn = None
    process = False
    creator_name = "stream"
    dbl_args = {}
    opts, args = getopt.getopt(sys.argv[1:], "u:p:fdvc:", ['process','batch-size=','no-db','follow=','track=','s3'])

    listeners = []
    follow = ()
    track = ()
    for o,a in opts:
        if o == '-u':
            usernames = a.split(',')
        elif o == '-p':
            password = a
        elif o == '-f':
            use_files = True
#        elif o == '-d':
#            conn = streamloader.connect_database()
#            print "Dumping stream to database (%s)" % str(conn)
        elif o == '--process':
            print 'Processing stream to database'
            process = True
        elif o == '--batch-size':
            dbl_args['batch_size'] = int(a)
        elif o == '--no-db':
            dbl_args['skipdb'] = True
        elif o == '--follow':
            follow = a.split(',')
        elif o == '--track':
            track = a.split(',')
        elif o == '-v':
            logging.getLogger('streamlistener').setLevel(logging.DEBUG)
        elif o == '-c':
            creator_name = a
        elif o == '--s3':
            uploader = S3StreamUploader(folder="twitter-stream", upload_interval=15)
            listeners.append(S3StoreListener(uploader=uploader))
    dbl_args['created_by'] = "%s:%s" % (creator_name, __version__)
#    if use_files or conn:
#        listeners.append(FileStreamListener(dump_file=use_files, conn=conn))
#        listeners.append(TweetStoreListener())
    if process:
        listeners.append(DbStreamListener(**dbl_args))
    if not listeners:
        print "Must select at least one of -f, or -d or --process."
        usage()
        sys.exit()

    streams = list()
    listener = AggregateUFListener(listeners)
    if not usernames:
        usernames = ['deepmile%s' % x for x in range(1,5)]
    start_streams(listener, password, streams, usernames, follow=follow, track=track)
    if not follow and not track:
        threading.Thread(target=watchdog, args=[listener, streams, usernames, password]).start()

def watchdog(listener, streams, usernames, password):
    print "Watchdog thread started"
    sleep_time = 30 # seconds
    while True:
        time.sleep(sleep_time)
        now = datetime.now()
        t = timedelta(seconds=600)
        if listener.last + t < now:
            # broken stream detected
            print "Watchdog activate! Streams dormant for %s seconds, reconnecting." % 600
            # Careful here, frequent reconnecting will get us banned.
            stop_streams(streams)
            start_streams(listener, password, streams, usernames)
        # check streams
        for stream in streams:
            if stream.last + timedelta(seconds=30) < now:
                print "Stream %s dormant for %s" % (stream.auth.username, now - stream.last)

if __name__ == '__main__':
    run()
