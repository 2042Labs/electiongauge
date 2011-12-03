import queue

def callback(data, message):
    print data

"""
To declare your own processor, either repurpose callback() or create another function just like that
and add it to the list of arguments to dequeue_loop().
"""

if __name__=="__main__":
    queue.dequeue_loop([callback])
