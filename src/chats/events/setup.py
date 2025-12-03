import os
import threading
import logging
from expertise_chats.broker import Consumer, BrokerConnection

from src.chats.dependencies.handlers import get_incomming_message_handler, get_outgoing_message_handler
logger = logging.getLogger("messages.events.setup")

AUTH_QUEUES = [
    ("messages.incomming", "messages.incomming.create")
    ("messages.outgoing", "messages.outgoing.send")
]

def __setup_messages_incomming_consumer():
    consumer = Consumer(
        queue_name="messages.incomming",
        handler=get_incomming_message_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("Messages incomming consumer listening")


def __setup_messages_outgoing_consumer():
    consumer = Consumer(
        queue_name="messages.outgoing",
        handler=get_outgoing_message_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("Messages outgoing consumer listening")


def __initialize_messages_queues():
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

    logger.info("Messages queues initialized")

    __setup_messages_incomming_consumer()
    __setup_messages_outgoing_consumer()




def initialize_messages_broker():
    __initialize_messages_queues()