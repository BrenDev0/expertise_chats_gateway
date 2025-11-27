import os
import jwt
from typing import Union, Dict, Any
import logging
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
logger = logging.getLogger(__name__)

token_key = os.getenv("TOKEN_KEY")

def decode_token(token: str) -> Union[Dict[str, Any], None]:
    token_key = os.getenv("TOKEN_KEY")
    if not token_key:
        raise ValueError("Web token secret not configured")
    
    try:
        return jwt.decode(token, token_key, algorithms=["HS256"])
    
    except jwt.ExpiredSignatureError:
        logger.warning(f"Token expired ::: {token}")
        raise ExpiredToken(f"Token expired ::: {token}")
        
    except jwt.InvalidTokenError:
        logger.warning(f"Invalid token ::: {token}")
        raise InvalidToken(f"Invalid token ::: {token}")