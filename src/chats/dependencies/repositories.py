import logging
from expertise_chats.dependencies.container import Container
from expertise_chats.exceptions.dependencies import DependencyNotRegistered

from src.chats.domain.repositories.message_repository import MessagesRepository
from  src.chats.infrastructure.sqlAlchemy.messages_repository import SqlAlchemyMessagesRepository
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.infrastructure.sqlAlchemy.chats_repository import SqlAchemyChatsRepsitory
from src.chats.domain.repositories.sessions_repository import SessionRepository
from src.chats.infrastructure.redis.session_repository import RedisSessionRepository
logger = logging.getLogger(__name__)

def get_sessions_repository() -> SessionRepository:
    try:
        instance_key = "sessions_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = RedisSessionRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")
    
    return repository


def get_messages_repository() -> MessagesRepository:
    try: 
        instance_key = "messages_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = SqlAlchemyMessagesRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository


def get_chats_repository() -> DataRepository:
    try: 
        instance_key = "chats_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = SqlAchemyChatsRepsitory()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")

    return repository