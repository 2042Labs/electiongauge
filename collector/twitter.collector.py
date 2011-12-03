import tweepy
import queue

username = "ElectionGauge"
password = "cssgmu"

def stream_starter(enqueue):
    class Listener(tweepy.StreamListener):
        def on_data(self, data):
            enqueue(data)
    auth = tweepy.auth.BasicAuthHandler(username, password)
    stream = tweepy.Stream(auth, listener=Listener())
    stream.sample()
    queue.LOG.info("Starting stream")

if __name__ == "__main__":
    queue.enqeue_loop(stream_starter)