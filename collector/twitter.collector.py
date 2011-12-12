import tweepy
import queue
try:
    import eventlet
    eventlet.monkey_patch()
except:
    pass

username = "ElectionGauge"
password = "cssgmu"

def stream_starter(enqueue):
    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            if data.startswith('{'):
                enqueue(data)
    auth = tweepy.auth.BasicAuthHandler(username, password)
    stream = tweepy.Stream(auth, listener=Listener())
    #stream.sample(async=True)
    stream.filter(track=open("candidates.txt").read().split(), follow=open("keywords.txt").read().split())
    print("Starting stream")

if __name__ == "__main__":
    queue.enqeue_loop(stream_starter)
