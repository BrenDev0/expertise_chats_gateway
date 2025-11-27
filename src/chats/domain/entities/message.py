from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime

class Message(BaseModel):
    message_id: Optional[UUID] = None
    chat_id: UUID
    sender: UUID # can be user_id or agent_id depending on message_type 
    text: Optional[str] = None
    json_data: Optional[Any] = None
    message_type: str
    created_at: Optional[datetime] = None