import tweepy
import queue

def stream_starter(enqueue):
    stream = tweepy.Stream(login, password, host, timeout)
    stream.stream(enqueue)

if __name__ == "__main__":
    queue.enqeue_loop(stream_starter)