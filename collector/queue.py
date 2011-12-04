# Common collector configuration

from kombu import BrokerConnection, Exchange, Queue
from kombu.common import maybe_declare
from kombu.pools import producers
import logging
import sys

CONN_STRING = "amqp://guest:guest@localhost:5672//"
CONN = BrokerConnection(CONN_STRING)
EXCHANGE = Exchange("eg-collector", type="direct", durable=True)
QUEUE = Queue("collector-consumer", exchange=EXCHANGE, durable=True, queue_arguments={"x-message-ttl":100000})

LOG = logging.getLogger("collector")
logging.basicConfig(level=logging.DEBUG)

# The queue API, in it simplest form:

def enqeue_loop(stream_starter):
    """
    Starts an enqueue loop. stream-starter will be passed a "enqueue" callback f(message) (that is,
    stream-starter is a callback itself).
    """
    with producers[CONN].acquire(block=True) as producer:
        maybe_declare(EXCHANGE, producer.channel)
        def callback(data):
            producer.publish(data, exchange=EXCHANGE)
        stream_starter(callback)

def dequeue_loop(callback):
    """
    This starts the consumer loop. Callback is a function of the form f(data, message).
    """
    callback = hasattr(callback, "__iter__") and callback or [callback]
    with BrokerConnection(CONN_STRING) as conn:
        with conn.Consumer(queues=QUEUE, callbacks=callback) as consumer:
            # Process messages and handle events on all channels
            while True:
                conn.drain_events()