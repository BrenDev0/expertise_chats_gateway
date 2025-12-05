from pydantic import BaseModel

class OutgoingMessage(BaseModel):
    llm_response: str