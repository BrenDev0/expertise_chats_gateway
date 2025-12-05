from typing import Union
import json
from uuid import UUID
from src.chats.domain.repositories.sessions_repository import SessionRepository
from src.chats.domain.repositories.message_repository import MessagesRepository
from src.chats.domain.entities.message import Message


class UpdateChatHistory:
    def __init__(
        self,
        session_repository: SessionRepository,
        messages_repository: MessagesRepository
    ):
        self.__sessions_repository = session_repository
        self.__messages_repository = messages_repository

    def execute(
        self,
        chat_id: Union[str, UUID],
        new_message: Message,
        exp_seconds: int = 3600
    ):
        session = self.__sessions_repository.get_session(
            key=str(chat_id)
        )

        if not session:
            chat_history = self.__messages_repository.get_many(
                key="chat_id",
                value=chat_id,
                limit=9
            ) or []

            chat_history = [new_message.model_dump(exclude={"chat_id", "sender", "message_id", "created_at"}, exclude_unset=False)]
        
        else: 
            chat_history = session
            chat_history.insert(0, new_message.model_dump(exclude={"chat_id", "sender", "message_id", "created_at"}, exclude_unset=False))

            if len(chat_history) > 10:
                chat_history.pop()
        
        self.__sessions_repository.set_session(
            key=str(chat_id),
            value=json.dumps(chat_history),
            expire_seconds=exp_seconds
        )
        return chat_history
        




        












