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
    stream = tweepy.Stream(auth, listener=Listener(), timeout=60, secure=True, retry_count=10)
    #stream.sample(async=True)
    stream.filter(track=open("candidates.txt").read().split(), follow=open("keywords.txt").read().split())
    print("Starting stream")

if __name__ == "__main__":
    queue.enqeue_loop(stream_starter)
