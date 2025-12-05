import logging
from typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, InteractionEvent, Producer
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.errors.error_handler import handle_error
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.chats.application.use_cases.create_message import CreateMessage

logger = logging.getLogger(__name__)

class IncommingMessageHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        create_message: CreateMessage,
        producer: Producer
    ):
        self.__create_message = create_message
        self.__producer = producer

    async def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Incomming message handler received request ::: {payload}")
        try:
            event = InteractionEvent(**payload)
            event_data = InteractionRequest(**event.event_data)

            message = self.__create_message.execute(
                chat_id=event.chat_id,
                sender_id=event.user_id,
                message_type="human",
                text=event_data.input
            )

            ws_payload = WsPayload(
                type="MESSAGE",
                data=message.model_dump()
            )

            event.event_data = ws_payload.model_dump()

            logger.debug(f"Publishing to streaming.general.outbound.send ::: {event.model_dump()}")
            ## send message data to front
            self.__producer.publish(
                routing_key="streaming.general.outbound.send",
                event_message=event
            )

            event.event_data = message.model_dump()

            logger.debug(f"Publishing to chats.history.update ::: {event.model_dump()}")
            ## update chat history
            self.__producer.publish(
                routing_key="chats.history.update",
                event_message=event
            )

        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.__producer,
                server_error=True
            )
            return 




