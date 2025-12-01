import logging
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
from src.auth.utils import decode_token
logger = logging.getLogger(__name__)

class ValidateToken:
    def __init__(self):
        pass


    def execute(
        self,
        token: str
    ):
        try:
            token_payload = decode_token(token=token)
            user_id = token_payload.get("user_id", None)
            company_id = token_payload.get("company_id", None)

            if not user_id or not company_id:
                raise InvalidToken()

        except ExpiredToken:
            raise
        
        except InvalidToken:
            raise
        
        except ValueError as e:
            logger.error(f"{str(e)}")
            raise InvalidToken(f"Token validation failed: {str(e)}")