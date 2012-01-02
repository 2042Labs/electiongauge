import queue
import simplejson as json
import cunning_linguist as cl
import sys
import geocoder
import logging as l
import traceback

from mapmaker import mapmaker
from timeline_maker import timeline_maker
from tweet_saver import tweet_saver
from discourse_mapper import discourse_mapper

geo=geocoder.geocoder()
out=file("/tmp/test_output.json",'ab')
mm=mapmaker(interval=10)
tm=timeline_maker(interval=10)
ts=tweet_saver("tweet",limit=1000,private=True)
proc=tweet_saver("processed",limit=1000,private=True)
dm = discourse_mapper(interval=10)

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
            
            l.log(l.DEBUG, ":)")
            
    except:
        #exc_type, exc_value, exc_traceback = sys.exc_info()
        #traceback.print_stack(exc_traceback)
        l.log(l.ERROR,":( >>" + str(sys.exc_info()))
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


