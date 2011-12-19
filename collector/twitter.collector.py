import tweepy
import queue
try:
    import eventlet
    eventlet.monkey_patch()
except:
    pass

username = "ElectionGauge"
password = "cssgmu"

CONSUMER_KEY = 'zSxtDpHrZ8GpSimb1k4DA'
CONSUMER_SECRET = 't1D97sSvjumR6iWLjvl1q95V0gs7ieWVyLJpzQAnBUw'
ACCESS_KEY = '365574554-eNVd7Xp8jYooqhXBEsd5xi7kCZqA6X7ZMNferWbV'
ACCESS_SECRET = 'nTIAxmLjaKa6oFHBj5ZbqBvofzuiM4YGYir7fyA5hc'

def stream_starter(enqueue):
    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            if data.startswith('{'):
                enqueue(data)
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    #stream.sample(async=True)
    track=open("candidates.txt").read().split()
    follow=open("keywords.txt").read().split()
    print("tracking %d and following %d" % (len(track),len(follow)))
    listener=Listener()
    stream = tweepy.Stream(auth, listener=listener, timeout=60, secure=True, retry_count=10)
    stream.filter(track=track, async=True)
    stream = tweepy.Stream(auth, listener=listener, timeout=60, secure=True, retry_count=10)
    stream.filter(follow=follow, async=True)
    print("Starting stream")

if __name__ == "__main__":
    queue.enqeue_loop(stream_starter)
