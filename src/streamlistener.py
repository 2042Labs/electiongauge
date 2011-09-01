import traceback
import simplejson
import tweepy
import time
from streamutil import dictize, mk_date
import streamloader
import threading
from collections import deque
import sys, os
import logging
from datetime import datetime

__author__ = 'Alex'
__version__ = "$Revision: 1286 $".split()[1]

LOG = logging.getLogger('streamlistener')
class NONLHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)
            fs = "%s"
            try:
                self.stream.write(fs % msg)
            except UnicodeError:
                self.stream.write(fs % msg.encode("UTF-8"))
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)

handler = NONLHandler()
handler.setFormatter(logging.Formatter('%(message)s'))
LOG.addHandler(handler)
LOG.propagate = False

class BenevolentStreamListener(tweepy.StreamListener):
    "Adheres to Twitter's prescribed back-off strategy."
    def __init__(self, *args, **kwargs):
        super(BenevolentStreamListener, self).__init__(*args, **kwargs)
        self._sleeptime = 10

    def on_error(self, status_code):
        print 'An error has occured! Status code %s, sleeping for %s' % (status_code, self._sleeptime)
        # Back off
        time.sleep(self._sleeptime)
        if self._sleeptime < (120 * 8):
            self._sleeptime *= 2
        return True # keep stream alive

    '''Strangely, running two concurrent streams in Python quickly shuts one of them down.
       In Jython no problem.'''
    def on_timeout(self):
        "From observation, hitting a timeout means the stream is dead."
        print 'Snoozing Zzzzzz'
        time.sleep(10)
        return True

    def on_delete(self, status_id, user_id):
        """Called when a delete notice arrives for a status"""
        #print "Delete notice for %s. %s" % (status_id, user_id)
        return

    def on_limit(self, track):
        """Called when a limitation notice arrvies"""
        print "!!! Limitation notice received: %s" % str(track)
        return

class BufferedStatusStreamListener(BenevolentStreamListener):
    '''Maintains an internal buffer for asynchronous processing.'''
    def __init__(self, *args, **kwargs):
        super(BufferedStatusStreamListener, self).__init__(*args, **kwargs)
        self.buffer = deque()
        self.buffer_event = threading.Event()
        threading.Thread(target=self._run).start()

    def _run(self):
        while True:
            if len(self.buffer) > 500:
                LOG.error('%s: queue length %s' % (self.__class__.__name__, len(self.buffer)))
            while len(self.buffer):
                data = self.buffer.popleft()
                if self.process(*data) is False:
                    return
            self.buffer_event.wait()
            self.buffer_event.clear()

    def on_status(self, status, raw):
        self.buffer.append((status, raw))
        self.buffer_event.set()

    def process(self, status, raw):
        '''Implement this instead of on_status()'''
        pass

class FileStreamListener(BenevolentStreamListener):

    def __init__(self, dump_file=True, conn=None, *args, **kwargs):
        super(FileStreamListener, self).__init__(*args, **kwargs)
        self.dumpcount = self.commitcount = 0
        self._dumpcutoff = 10000 # tweets per file
        self._commitcutoff = 300 # tweets per commit
        self.outfile = None
        self.dump_file = dump_file
        self.raw_inserter = None
        if conn:
            self.raw_inserter = streamloader.RawInserter(conn=conn)

    def dump(self, tweetstr):
        if self.outfile and self.dumpcount >= self._dumpcutoff:
            self.outfile.close()
            self.outfile = None
            self.dumpcount = 0
        if not self.outfile:
            fname = 'tweets.v%s.%s' % (__version__, time.time())
            print '> ' + fname
            self.outfile = open(fname, 'w')
        self.outfile.write(tweetstr)
        #self.outfile.write('\n')
        self.outfile.flush()
        self.dumpcount += 1

    def on_status(self, status, raw):
        try:
            dic = dictize(status, lambda k,v: k not in ['_api','author'])
            #str = simplejson.dumps(dic, indent=2, sort_keys=True)
            if self.dump_file:
                self.dump(raw)
            if self.raw_inserter:
                self.raw_inserter.insert_raw_tweet(raw, data=dic, version='stream:%s'%__version__)
        except Exception, e:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass


class ParallelAsyncStreamListener(BenevolentStreamListener):
    'Listen to stream and process batches in parallel'
    def __init__(self, batch_size=30, buffer_limit=500, pool_size=10, *args, **kwargs):
        super(ParallelAsyncStreamListener, self).__init__(*args, **kwargs)
        self._batch_size = batch_size
        self._buffer_limit = buffer_limit
        self._pool_size = pool_size

        self.buffer = deque()
        self.buffer_condition = threading.Condition() # signaled when buffer threshold is crossed
        self.buffer_ready_event = threading.Event()
        self._stop = threading.Event()

        self.pool = [threading.Thread(target=self.run,
                                     name=str(x)) for x in range(pool_size)]

        self.batch = list()
        LOG.info("Starting %s worker threads.\n" % self._pool_size)
        for thread in self.pool:
            thread.start()
        threading.Thread(target=self._relay_event).start()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        _name = threading.currentThread().getName()
        while not self.stopped():
            try:
                # Get lock and dequeue
                self.buffer_condition.acquire()
                while not len(self.buffer):
                    self.buffer_condition.wait(2)
                LOG.debug('* Worker %s awake, buffer size %s\n' % (_name, len(self.buffer)))
                batch = self.buffer.popleft()
                self.buffer_condition.release()

                # Process
                self.process(batch)

                LOG.debug('* Worker %s finished.\n' % _name)
            except Exception,e:
                LOG.error('* Worder %s had a problem: %s' % (_name, e))
                traceback.print_exc()

    def _relay_event(self):
        while True:
            self.buffer_ready_event.wait()
            LOG.debug('!')
            self.buffer_ready_event.clear()
            self.buffer_condition.acquire()
            self.buffer_condition.notifyAll()
            self.buffer_condition.release()

    def _enqueue(self, status, raw):
        self.batch.append((status, raw))
        if len(self.batch) >= self._batch_size:
            LOG.debug('+')
            if len(self.buffer) > self._buffer_limit:
                LOG.error("Buffer over limit (%s), skipping batch.\n" % len(self.buffer))
            else:
                self.buffer.append(self.batch)
                self.buffer_ready_event.set()
            self.batch = list() # Start a new batch


    def on_status(self, status, raw):
        try:
            if self._stop.isSet():
                return False    # this is the end

            # dictize because the other code expects dictionaries (previosly created from stored JSON)
            # TODO: use status object directly, no need to dictize anymore
            dic = dictize(status, lambda k,v: k not in ['_api','author'])
            self._enqueue(dic, raw)
        except Exception:
            traceback.print_exc()

    def process(self, batch_of_tweets):
        'Override this. Use thread local storage to persist thread local data!'
        pass


class DbStreamListener(ParallelAsyncStreamListener):
    def __init__(self,
                 skipdb=False,
                 created_by='streamlistener:%s'%__version__,
                 reprocess=False,
                 *args, **kwargs):
        super(DbStreamListener, self).__init__(*args, **kwargs)
        self.skipdb = skipdb
        if skipdb:
            LOG.warning("DbStreamListener initialized with skipdb, not touching the database.")
        self.data = threading.local()
        self.created_by = created_by
        self.reprocess = reprocess

    def process(self, batch):
        data = self.data
        if not hasattr(data,'conn'):
            print "Worker %s connecting to database." % threading.currentThread().getName()
            if not self.skipdb:
                data.conn = streamloader.connect_database()
            else:
                data.conn = None
                
        if data.conn:
            #read_cursor = data.conn.cursor()
            insert_cursor = data.conn.cursor()
            processed = False
            for item in batch:
                tweet, raw = item
                try:
                    if streamloader.insert_processed_tweet(tweet,
                                                           cursor=insert_cursor, raw=raw,
                                                           created_by=self.created_by):
                        streamloader.process_user(insert_cursor,
                                                  insert_cursor,
                                                  tweet['user'])
                        streamloader.process_entities(insert_cursor, tweet)
                        processed = True
                except Exception,e:
                    traceback.print_exc()
                    if not self.reprocess:
                        print "Worker %s had a problem, dumping batch." % threading.currentThread().getName()
                    else:
                        print "Worker %s had a problem, requeuing batch." % threading.currentThread().getName()
                        batch.remove(item)
                        self.buffer.append(self.batch)
                        self.buffer_ready_event.set()
                    insert_cursor.connection.rollback()
                    break
            if processed:
                insert_cursor.execute("update status set property_last_updated=now() where property_name='last_tweet_processed_date'")
            insert_cursor.connection.commit()
            insert_cursor.close()

class S3StoreListener(BufferedStatusStreamListener):
    def __init__(self, uploader, *args, **kwargs):
        self.uploader = uploader
        super(S3StoreListener, self).__init__(*args, **kwargs)

    def process(self, status, raw):
        self.uploader.put(raw, raw=True)

class AggregateUFListener(BenevolentStreamListener):
    'Multiple listeners, with unique tweet prefiltering'
    def __init__(self, listeners = [], stay_alive = False):
        super(AggregateUFListener, self).__init__()
        self.listeners = listeners
        self.stay_alive = stay_alive

        self.unique_list = deque()
        self.unique_set = set()
        self.unique_lock = threading.Lock()
        self._unique_set_limit = 9000 # remember last X tweets

    def _is_unique(self, id):
        ''' Rememeber last self._unique_set_limit tweets. '''
        ret = False
        if self.unique_lock.acquire():
            try:
                while len(self.unique_list) > self._unique_set_limit:
                    self.unique_set.remove(self.unique_list.popleft())
            except:
                LOG.debug('>')

            if id not in self.unique_set:
                self.unique_list.append(id)
                self.unique_set.add(id)
                ret = True
            self.unique_lock.release()
        return ret

    def on_status(self, status, raw):
        try:
            self.last = datetime.now()
            LOG.debug('.')
            if not self._is_unique(status.id):
                LOG.debug('x')
                return True

            for listener in self.listeners:
                success = False
                try:
                    success = listener.on_status(status, raw)
                except:
                    pass
                # Here we get to decide what to do with the flake
                if success is False:
                    LOG.error("Listener %s has failed, removing." % listener)
                    self.listeners.remove(listener)
            if not self.listeners and not self.stay_alive:
                # They're all gone and that's sad.
                LOG.info("No more listeners left, quitting.")
                return False # bye-bye, stream
        except:
            traceback.print_exc()
