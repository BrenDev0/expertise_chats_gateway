from pydantic import BaseModel

class LlmChunk(BaseModel):
    chunk: str
