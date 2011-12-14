import queue
import simplejson as json
import cunning_linguist as cl
import sys
import wordbag
import geocoder

bag=wordbag.wordbag()
geo=geocoder.geocoder()

def callback(data, message):
    js = None
    if data.startswith('{'):
        js=json.loads(data)
        #print '.',
 #   try :
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
        if len(tokens)>0:
            bag.add_tokens('stream',tokens)
        else:
            return           
            
        js_out=json.dumps({'tokens':tokens, 'geo':place})
        
        print js_out
            
#   except:
#        print ":(", sys.exc_info()
#        pass
#    finally:
#        if message is not None:
#            message.ack()


def test():
    file="data.json"
    for line in open(file,'rb'):
        print '>',
        callback(line,None)

"""
To declare your own processor, either repurpose callback() or create another function just like that
and add it to the list that is the first argument to dequeue_loop().
"""

if __name__=="__main__":
    queue.dequeue_loop([callback])


