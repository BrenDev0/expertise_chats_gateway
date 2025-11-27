import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.chats.events.handlers.incomming_message import IncommingMessageHandler
from src.chats.dependencies.use_cases import get_create_message_use_case
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

    return handler
