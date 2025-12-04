from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.entities.chat import Chat
from src.chats.domain.schemas.chats import ChatPublic, ChatUpdate

class UpdateChat:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        chat_id: UUID,
        changes: ChatUpdate
    ):
        chat = self.__repository.get_one(
            key="chat_id",
            value=chat_id
        )

        if not chat:
            pass