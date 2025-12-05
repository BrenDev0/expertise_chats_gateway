from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.entities.chat import Chat
from src.chats.domain.schemas.chats import ChatPublic, ChatCreate

class CreateChat:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        user_id: UUID,
        chat_data: ChatCreate
    ):
        data = Chat(**chat_data)
        data.user_id = user_id

        new_chat = self.__repository.create(data=data)
        
        return ChatPublic.model_validate(new_chat, from_attributes=True)