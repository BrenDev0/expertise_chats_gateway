import logging
from typing import Dict, Any
from expertise_chats.broker import InteractionEvent, EventHandlerBase, Producer
from expertise_chats.errors.error_handler import handle_error
from src.chats.application.use_cases.create_message import CreateMessage
from src.chats.domain.schemas.messages import OutgoingMessage

logger = logging.getLogger(__name__)

class OutgoingMessageHandler(EventHandlerBase):
    def __init__(
        self,
        create_message: CreateMessage,
        producer: Producer
    ):
        self.__create_message = create_message
        self.__producer = producer

    def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Outgoing message handler received request ::: {payload}")

        try:
            event = InteractionEvent(**payload)
            event_data = OutgoingMessage(**event.event_data)

            message = self.__create_message.execute(
                chat_id=event.chat_id,
                sender_id=event.user_id,
                message_type="ai",
                text=event_data.llm_response
            )

            event.turn_complete = True
            event.event_data = message.model_dump()

            logger.debug(f"Publishing to sessions.chat_history.update ::: {event}")
            ## update chat history
            self.__producer.publish(
                routing_key="sessions.chat_history.update",
                event_message=event
            )

        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.__producer,
                server_error=True
            )
