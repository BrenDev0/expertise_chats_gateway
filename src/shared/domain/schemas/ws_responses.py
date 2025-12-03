from pydantic import BaseModel
from typing import Union, Dict, Any, Optional

class RequestErrorBase(BaseModel):
    error: str
    detail: str
    additional_info: Optional[Union[str, Dict[str, Any]]] = None
