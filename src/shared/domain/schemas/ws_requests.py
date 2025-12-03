from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class InteractionRequest(BaseModel):
    token: str
    agent_id: UUID
    input: str
    voice: Optional[bool] = False

    model_config = ConfigDict(
        extra="forbid"
    )
    

