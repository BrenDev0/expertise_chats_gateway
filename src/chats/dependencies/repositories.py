import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.chats.domain.repositories.message_repository import MessagesRepository
from  src.chats.infrastructure.sqlAlchemy.messages_repository import SqlAlchemyMessagesRepository
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.infrastructure.sqlAlchemy.chats_repository import SqlAchemyChatsRepsitory
logger = logging.getLogger(__name__)

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