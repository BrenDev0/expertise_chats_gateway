import logging
from typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, Producer, BaseEvent, InteractionEvent
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
from src.auth.domain.schemas import AuthError
from src.shared.domain.schemas.ws_responses import WsPayload
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.auth.application.use_cases.validate_credentials import ValidateCredentials
from src.auth.application.use_cases.validate_token import ValidateToken
logger = logging.getLogger(__name__)

class AuthHandler(AsyncEventHandlerBase):
    def __init__(
        self, 
        producer: Producer,
        validate_token: ValidateToken,
        validate_credentials: ValidateCredentials
    ):
        self.__producer = producer
        self.__validate_token = validate_token
        self.__validate_credentials = validate_credentials

    async def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
        event_data = InteractionRequest(**event.event_data)
        
        try:
            token_payload = self.__validate_token.execute(
                token=event_data.token
            )
            user_id = token_payload.get("user_id", None)
            company_id = token_payload.get("company_id", None)

            self.__validate_credentials.execute(
                company_id=company_id,
                user_id=user_id
            )

            interaction_event = InteractionEvent(
                chat_id=event.chat_id,
                user_id=user_id,
                company_id=company_id,
                agent_id=event_data.agent_id,
                voice=event_data.voice,
                event_data=event_data
            )
            
            self.__producer.publish(
                routing_key="messages.incoming.create",
                event_message=interaction_event
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
        
        except AuthError as e:
            ws_payload = WsPayload(
                type="ERROR",
                data=e.model_dump()
            )

            event.event_data = ws_payload

            self.__producer.publish(
                routing_key="streaming.general.outbound.send",
                event_message=event
            )

            return 
        
        except ValueError as e:
            logger.error(f"{str(e)}")
