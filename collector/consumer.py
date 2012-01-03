import queue
import simplejson as json
import cunning_linguist as cl
import sys
import geocoder
import logging
import traceback

l=logging.getLogger("CONSUMER")

from mapmaker import mapmaker
from timeline_maker import timeline_maker
from tweet_saver import tweet_saver
from discourse_mapper import discourse_mapper



##### INITIALIZE MAJOR COMPONENTS
geo=geocoder.geocoder()
out=file("/tmp/test_output.json",'ab')
mm=mapmaker(interval=100)
tm=timeline_maker(interval=100)
ts=tweet_saver("tweet",limit=1000,private=False)
proc=tweet_saver("processed",limit=1000,private=False)
dm = discourse_mapper(interval=100)



#### SET UP LOG LEVELS #####
logging.getLogger("boto").setLevel(logging.INFO)
logging.getLogger("geopy").setLevel(logging.INFO)
logging.getLogger("GEOCODER").setLevel(logging.INFO)
logging.getLogger("MAPMAKER").setLevel(logging.INFO)
logging.getLogger("GEOCODER").setLevel(logging.INFO)
logging.getLogger("TIMELINE").setLevel(logging.INFO)
logging.getLogger("TWEET_SAVER").setLevel(logging.INFO)
logging.getLogger("DMAP").setLevel(logging.DEBUG)
logging.getLogger("CONSUMER").setLevel(logging.DEBUG)



def callback(data, message):
    js = None
    if data.startswith('{'):
        js=json.loads(data)
        #print '.',
    try :
        if js:
        
            try :
                text=js['text']
            except KeyError:
                return

            #geocode what we can and throw away what can't be saved
            place=geo.geocode(js)
            if place==None or place==[]:
                return

            tokens=cl.process(text)
            if len(tokens)==0:
                return           
            
            ts.add(data)
            
            js_out=json.dumps({'tokens':tokens, 'geo':place})+"\n"
            #out.write(js_out)
            proc.add(js_out)
            
            ##Map buzz of candidates per zip code
            mm.add_to_map(place,tokens)
            
            ##Add tweet to the timeline
            tm.add_to_timeline(tokens)
            
            ## add tokens to the discourse mapper
            dm.add(place,tokens)
            
            l.debug(".")
            
    except:
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_stack(exc_traceback)
        l.error(":( >>" + str(sys.exc_info()))
        pass
    finally:
        if message is not None:
            message.ack()


def test():
    file="data.json"
    for line in open(file,'rb'):
        callback(line,None)

"""
To declare your own processor, either repurpose callback() or create another function just like that
and add it to the list that is the first argument to dequeue_loop().
"""

if __name__=="__main__":
    queue.dequeue_loop([callback])


