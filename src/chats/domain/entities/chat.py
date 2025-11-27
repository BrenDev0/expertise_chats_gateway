from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Chat(BaseModel):
    chat_id: Optional[UUID] = None
    user_id: UUID
    title: Optional[str] = None