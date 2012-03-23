import tweepy
import queue
#try:
#    import eventlet
#    eventlet.monkey_patch()
#except:
#    pass

username = "ElectionGauge"
password = "cssgmu"

CONSUMER_KEY = 'zSxtDpHrZ8GpSimb1k4DA'
CONSUMER_SECRET = 't1D97sSvjumR6iWLjvl1q95V0gs7ieWVyLJpzQAnBUw'
ACCESS_KEY = '365574554-eNVd7Xp8jYooqhXBEsd5xi7kCZqA6X7ZMNferWbV'
ACCESS_SECRET = 'nTIAxmLjaKa6oFHBj5ZbqBvofzuiM4YGYir7fyA5hc'

follow=open("candidates.ids").read().split()
track=open("keywords.txt").read().split()

def stream_starter(enqueue):
    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            if data.startswith('{'):
                enqueue(data)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    #stream.sample(async=True)
    print("tracking %d and following %d" % (len(track),len(follow)))
    listener=Listener()
    stream = tweepy.Stream(auth, listener=listener, timeout=60, secure=True, retry_count=10)
    stream.filter(track=track, async=True)
    stream = tweepy.Stream(auth, listener=listener, timeout=60, secure=True, retry_count=10)
    stream.filter(follow=follow, async=True)
    print("Starting stream")

import requests
def rstream_starter(enqueue):
    data = {"follow": follow, "track": track}
    r = requests.post('https://stream.twitter.com/1/statuses/filter.json',
	    data=data, auth=(username, password))
    for line in r.iter_lines():
	if line:
	    enqueue(line)

if __name__ == "__main__":
    queue.enqeue_loop(rstream_starter)
