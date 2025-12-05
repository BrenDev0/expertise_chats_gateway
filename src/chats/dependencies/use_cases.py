import logging
from expertise_chats.dependencies.container import Container
from expertise_chats.exceptions.dependencies import DependencyNotRegistered

from src.chats.application.use_cases.create_message import CreateMessage
from src.chats.application.use_cases.update_chat_history import UpdateChatHistory
from src.chats.application.use_cases.create_chat import CreateChat
from src.chats.application.use_cases.update_chat import UpdateChat
from src.chats.dependencies.repositories import get_messages_repository, get_sessions_repository, get_chats_repository
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
        logger.info(f"{instance_key} registered")

    return use_case

def get_update_chat_history_use_case() -> UpdateChatHistory:
    try: 
        instance_key = "update_chat_history_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = UpdateChatHistory(
            messages_repository=get_messages_repository(),
            session_repository=get_sessions_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_create_chat_use_case() -> CreateChat:
    try: 
        instance_key = "create_chat_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = CreateChat(
            repository=get_chats_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_update_chat_use_case() -> UpdateChat:
    try: 
        instance_key = "update_chat_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = UpdateChat(
            repository=get_chats_repository()
        )
        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

