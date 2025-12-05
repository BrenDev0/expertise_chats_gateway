import logging
from typing import Dict, Any
from expertise_chats.broker import EventHandlerBase, Producer, BaseEvent, InteractionEvent
from expertise_chats.errors.error_handler import handle_error
from expertise_chats.schemas.ws import RequestErrorBase
from src.auth.domain.exceptions import ExpiredToken, InvalidToken
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
        logger.debug(f"Auth handler received request ::: {payload}")
        
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
                chat_id=str(event.chat_id),
                user_id=str(user_id),
                company_id=str(company_id),
                agent_id=str(event_data.agent_id),
                voice=event_data.voice,
                event_data=event_data.model_dump()
            )
            logger.debug(f"Publishing to messages.incomming.create ::: {interaction_event.model_dump()}")
            self.__producer.publish(
                routing_key="messages.incomming.create",
                event_message=interaction_event
            )

        except ExpiredToken:
            error = RequestErrorBase(
                error="Authorization Error",
                detail="Expired token",
                additional_info=str(event_data.token)
            )

            handle_error(
                event=event,
                producer=self.__producer,
                error=error
            )

            return 
        
        except InvalidToken:
            error = RequestErrorBase(
                error="Authorization Error",
                detail="Invalid token",
                additional_info=str(event_data.token)
            )

            handle_error(
                event=event,
                producer=self.__producer,
                error=error
            )

            return 
        
        except AuthError as e:
            error = RequestErrorBase(
                error=e.error,
                detail=e.detail,
                additional_info=e.additional_info
            )

            handle_error(
                event=event,
                producer=self.__producer,
                error=error
            )
            return 
        
        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.__producer,
                server_error=True
            )

            return 
