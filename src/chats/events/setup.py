import os
import threading
import logging
from expertise_chats.broker import Consumer, BrokerConnection

from src.chats.dependencies.handlers import get_incomming_message_handler, get_outgoing_message_handler, get_chat_history_handler, get_generate_chat_title_handler
logger = logging.getLogger("messages.events.setup")

AUTH_QUEUES = [
    ("messages.incomming", "messages.incomming.create"),
    ("messages.outgoing", "messages.outgoing.send"),
    ("chats.history", "chats.history.update"),
    ("chats.title", "chats.title.generate")
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


def __setup_chat_history_consumer():
    consumer = Consumer(
        queue_name="chats.history",
        handler=get_chat_history_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("Chat history consumer listening")


def __setup_chat_title_generator_consumer():
    consumer = Consumer(
        queue_name="chats.title",
        handler=get_generate_chat_title_handler()
    )
    
    thread = threading.Thread(target=consumer.start, daemon=True)
    thread.start()
    logger.info("Chat title generator consumer listening")


def __initialize_chats_queues():
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
    __setup_chat_history_consumer()
    __setup_chat_title_generator_consumer()




def initialize_messages_broker():
    __initialize_chats_queues()