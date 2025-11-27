import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.chats.application.use_cases.create_message import CreateMessage
from src.chats.dependencies.repositories import get_messages_repository
logger = logging.getLogger(__name__)

def get_create_message_use_case() -> CreateMessage:
    try: 
        instance_key = "create_message_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = CreateMessage(
            repository=get_messages_repository()
        )
        Container.register(instance_key, use_case)

    return use_case
