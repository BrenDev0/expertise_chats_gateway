from uuid import UUID
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.schemas.chats import ChatPublic, ChatUpdate
from src.shared.domain.exceptions.not_found import NotFoundException

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
    ) -> ChatPublic:
        chat = self.__repository.get_one(
            key="chat_id",
            value=chat_id
        )

        if not chat:
            raise NotFoundException(detail=f"Chat with id {chat_id} not found")
        
        updated_chat = self.__repository.update(
            key="chat_id", 
            value=chat_id, 
            changes=changes.model_dump(exclude_unset=True)
        )
    
        return ChatPublic.model_validate(updated_chat, from_attributes=True)
        
