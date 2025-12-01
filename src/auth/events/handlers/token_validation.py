import logging
from typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, BaseEvent, Producer
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
from src.auth.domain.schemas import AuthError
from src.shared.domain.schemas.ws_responses import WsPayload
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.auth.utils import decode_token
logger = logging.getLogger(__name__)

class AuthHandler(AsyncEventHandlerBase):
    def __init__(self, producer: Producer):
        self.__producer = producer

    async def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
        event_data = InteractionRequest(**event.event_data)
        
        try:
            token_payload = decode_token(token=event_data.token)
            user_id = token_payload.get("user_id", None)
            company_id = token_payload.get("company_id", None)

            if not user_id or not company_id:
                raise InvalidToken()

            self.__producer.publish(
                routing_key="messages.incoming.create",
                event_message=event
            )

        except ExpiredToken:
            error = AuthError(
                error="Authorization Error",
                detail="Expired token",
                additional_info=str(event_data.token)
            )

            ws_payload = WsPayload(
                type="ERROR",
                data=error.model_dump()
            )

            event.event_data = ws_payload

            self.__producer.publish(
                routing_key="streaming.general.outbound.send",
                event_message=event
            )

            return 
        
        except InvalidToken:
            error = AuthError(
                error="Authorization Error",
                detail="Invalid token",
                additional_info=str(event_data.token)
            )

            ws_payload = WsPayload(
                type="ERROR",
                data=error.model_dump()
            )

            event.event_data = ws_payload

            self.__producer.publish(
                routing_key="streaming.general.outbound.send",
                event_message=event
            )

            return 
        
        except ValueError as e:
            logger.error(f"{str(e)}")
