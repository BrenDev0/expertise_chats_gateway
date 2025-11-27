import os
import threading
import logging
from expertise_chats.broker import Consumer, BrokerConnection

from src.auth.dependencies.handlers import get_auth_handler
logger = logging.getLogger("auth.events.setup")

AUTH_QUEUES = [
    ("auth.validation", "auth.validation.validate")
]

def __setup_auth_validation_consumer():
    consumer = Consumer(
        queue_name="auth.validation",
        handler=get_auth_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("auth validation consumer listening")


def initialize_auth_queues():
    EXCHANGE = os.getenv("EXCHANGE")
    channel = BrokerConnection.get_channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="topic",
        durable=True
    )


    for queue_name, routing_key in AUTH_QUEUES:
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(
            exchange=EXCHANGE,
            queue=queue_name,
            routing_key=routing_key
        )

    logger.info("General streaming queue initialized")

    __setup_auth_validation_consumer()