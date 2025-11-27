from uuid import UUID
from abc import abstractmethod
from typing import List

from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.entities.message import Message

class MessagesRepository(DataRepository[Message]):
    @abstractmethod
    def search_by_content(
        self,
        content: str, 
        user_id: UUID
    ) -> List[Message]:
        raise NotImplementedError
        
