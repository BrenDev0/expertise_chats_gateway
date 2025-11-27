import os
import threading
import logging
from expertise_chats.broker import Consumer, BrokerConnection

from src.streaming.dependencies.handlers import get_general_streaming_handler
logger = logging.getLogger("features.sessions.setup")

GENERAL_STREAMING_QUEUES = [
    ("streaming.general", "streaming.general.outbound.send")
]

def __setup_general_streaming_outbound_consumer():
    consumer = Consumer(
        queue_name="streaming.audio.outbound",
        handler=get_general_streaming_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("General streaming outbound consumer listening")


def initialize_general_streaming_queues():
    EXCHANGE = os.getenv("EXCHANGE")
    channel = BrokerConnection.get_channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )


    for queue_name, routing_key in GENERAL_STREAMING_QUEUES:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(
            exchange=EXCHANGE,
            queue=queue_name,
            routing_key=routing_key
        )

    logger.info("General streaming queue initialized")

    __setup_general_streaming_outbound_consumer()