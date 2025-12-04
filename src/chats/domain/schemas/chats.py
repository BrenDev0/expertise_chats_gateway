from pydantic import BaseModel, ConfigDict
from  uuid import UUID 
from pydantic.alias_generators import to_camel


class ChatConfig(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        serialize_by_alias=True,
        alias_generator=to_camel,
        extra="forbid"
    )

class ChatCreate(ChatConfig):
    title: str

class ChatUpdate(ChatConfig):
    title: str

class ChatPublic(ChatCreate):
    chat_id: UUID
    user_id: UUID
      
class ChatCreateResponse(ChatConfig):
    chat_id: UUID

class GenerateChatTitle(ChatCreateResponse):
    pass

