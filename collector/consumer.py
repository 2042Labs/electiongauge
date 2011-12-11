import queue
import simplejson as json
import cunning_linguist as cl
import sys

def callback(data, message):
    js = None
    if data.startswith('{'):
        js=json.loads(data)
        print '.',
    try :
        if js:
            text=js['text']
            tokens=cl.process(text)
            if len(tokens)>0:
                print tokens 
    except:
        print ":(", sys.exc_info()
        pass
    finally:
        message.ack()



"""
To declare your own processor, either repurpose callback() or create another function just like that
and add it to the list that is the first argument to dequeue_loop().
"""

if __name__=="__main__":
    queue.dequeue_loop([callback])


