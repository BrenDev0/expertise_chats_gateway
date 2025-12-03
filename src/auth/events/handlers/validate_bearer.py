import logging
from typing import Dict, Any
from expertise_chats.broker import EventHandlerBase, Producer, BaseEvent, InteractionEvent
from expertise_chats.schemas.ws import WsPayload
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
from src.shared.domain.schemas.ws_responses import RequestErrorBase
from src.auth.domain.exceptions import AuthError
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.auth.application.use_cases.validate_credentials import ValidateCredentials
from src.auth.application.use_cases.validate_token import ValidateToken
logger = logging.getLogger(__name__)

class AuthHandler(EventHandlerBase):
    def __init__(
        self, 
        producer: Producer,
        validate_token: ValidateToken,
        validate_credentials: ValidateCredentials
    ):
        self.__producer = producer
        self.__validate_token = validate_token
        self.__validate_credentials = validate_credentials

    def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
        event_data = InteractionRequest(**event.event_data)
        
        try:
            token_payload = self.__validate_token.execute(
                token=event_data.token
            )
            logger.debug(f"token validated")
            user_id = token_payload.get("user_id", None)
            company_id = token_payload.get("company_id", None)

            self.__validate_credentials.execute(
                company_id=company_id,
                user_id=user_id
            )
            logger.debug(f"Credentials validated")

            interaction_event = InteractionEvent(
                chat_id=str(event.chat_id),
                user_id=str(user_id),
                company_id=str(company_id),
                agent_id=str(event_data.agent_id),
                voice=event_data.voice,
                event_data=event_data.model_dump()
            )
            logger.debug("to publish")
            self.__producer.publish(
                routing_key="messages.incoming.create",
                event_message=interaction_event
            )

        except ExpiredToken:
            error = RequestErrorBase(
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
            error = RequestErrorBase(
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
            error = RequestErrorBase(
                error=e.error,
                detail=e.detail,
                additional_info=e.additional_info
            )
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
