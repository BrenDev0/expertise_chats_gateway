from uuid import UUID
from typing import Any
from src.chats.domain.repositories.message_repository import MessagesRepository
from src.chats.domain.entities.message import Message

class CreateMessage:
    def __init__(
        self,
        repository: MessagesRepository
    ):
        self.__repository = repository

    
    def execute(
        self,
        chat_id: UUID, 
        sender_id: UUID, 
        message_type: UUID, 
        text: str = None,
        json_data: Any = None
    ) -> Message:
        data = Message(
            chat_id=chat_id,
            sender=sender_id,
            text=text,
            message_type=message_type,
            json_data=json_data
        )

        return self.__repository.create(data=data)

