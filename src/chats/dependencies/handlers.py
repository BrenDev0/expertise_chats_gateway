import logging
from expertise_chats.dependencies.container import Container
from expertise_chats.exceptions.dependencies import DependencyNotRegistered
from src.chats.events.handlers.incomming_message import IncommingMessageHandler
from src.chats.events.handlers.outgoing_message import OutgoingMessageHandler
from src.chats.events.handlers.update_chat_history import UpdateChatHistoryHandler
from src.chats.dependencies.use_cases import get_create_message_use_case, get_update_chat_history_use_case
from src.shared.dependencies.producers import get_producer
logger = logging.getLogger(__name__)

def get_incomming_message_handler() -> IncommingMessageHandler:
    try:
        instance_key = "incomming_message_handler"
        handler = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        handler = IncommingMessageHandler(
            create_message=get_create_message_use_case(),
            producer=get_producer()
        )
        Container.register(instance_key, handler)
        logger.info(f"{instance_key} registered")

    return handler

def get_outgoing_message_handler() -> OutgoingMessageHandler:
    try:
        instance_key = "outgoing_message_handler"
        handler = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        handler = OutgoingMessageHandler(
            create_message=get_create_message_use_case(),
            producer=get_producer()
        )
        Container.register(instance_key, handler)
        logger.info(f"{instance_key} registered")

    return handler

def get_outgoing_message_handler() -> OutgoingMessageHandler:
    try:
        instance_key = "outgoing_message_handler"
        handler = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        handler = OutgoingMessageHandler(
            create_message=get_create_message_use_case(),
            producer=get_producer()
        )
        Container.register(instance_key, handler)
        logger.info(f"{instance_key} registered")

    return handler


def get_chat_history_handler() -> UpdateChatHistoryHandler:
    try:
        instance_key = "update_history_handler"
        handler = Container.resolve(instance_key)
    
    except DependencyNotRegistered:
        handler = UpdateChatHistoryHandler(
            update_chat_history=get_update_chat_history_use_case(),
            producer=get_producer()
        )
        
        Container.register(instance_key, handler)
        logger.info(f"{instance_key} registered")

    return handler

