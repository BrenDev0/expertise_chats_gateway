from pydantic import BaseModel
from typing import Union, Dict, Any, Optional

class WsPayload(BaseModel):
    type: str
    data: Union[str, Dict[str, Any]]

class RequestErrorBase(BaseModel):
    error: str
    detail: str
    additional_info: Optional[Union[str, Dict[str, Any]]] = None
