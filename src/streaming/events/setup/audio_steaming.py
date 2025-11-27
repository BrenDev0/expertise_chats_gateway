import os
import threading
import logging
from expertise_chats.broker import Consumer, BrokerConnection

from src.streaming.dependencies.handlers import get_audio_streaming_handler
logger = logging.getLogger("features.sessions.setup")

AUDIO_STREAMING_QUEUES = [
    ("streaming.audio.outbound", "streaming.audio.outbound.send")
]

def __setup_audio_streaming_outbound_consumer():
    consumer = Consumer(
        queue_name="streaming.audio.outbound",
        handler=get_audio_streaming_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("Audio streaming outbound consumer listening")


def initialize_audio_streaming_queues():
    EXCHANGE = os.getenv("EXCHANGE")
    channel = BrokerConnection.get_channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )


    for queue_name, routing_key in AUDIO_STREAMING_QUEUES:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(
            exchange=EXCHANGE,
            queue=queue_name,
            routing_key=routing_key
        )

    logger.info("Audio streaming queue initialized")

    __setup_audio_streaming_outbound_consumer()