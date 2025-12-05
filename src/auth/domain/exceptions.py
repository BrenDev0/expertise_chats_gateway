from typing import Dict, Any, Union

class ExpiredToken(Exception):
    def __init__(self, detail: str = "Token expired"):
        super().__init__(detail)

class InvalidToken(Exception):
    def __init__(self, detail: str = "Ivalid token"):
        super().__init__(detail)

class AuthError(Exception):
    def __init__(self, detail: str, error: str, additional_info: Union[Dict[str, Any], str] = None):
        super().__init__(detail)
        self.detail = detail
        self.error = error
        self.additional_info = additional_info
        
