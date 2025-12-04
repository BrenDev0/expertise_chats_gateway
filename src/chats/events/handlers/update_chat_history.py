import logging
from typing import Dict, Any
from expertise_chats.broker import EventHandlerBase, InteractionEvent
from expertise_chats.errors.error_handler import handle_error
from src.chats.application.use_cases.update_chat_history import UpdateChatHistory
from expertise_chats.broker import Producer
from src.chats.domain.entities.message import Message

logger = logging.getLogger(__name__)

class UpdateChatHistoryHandler(EventHandlerBase):
    def __init__(
        self,
        producer: Producer,
        update_chat_history: UpdateChatHistory
    ):
        self.___producer = producer
        self.__update_chat_history = update_chat_history

    def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Update chat history handler received request ::: {payload}")
        try:
            event = InteractionEvent(**payload)
            message = Message(**event.event_data)

            chat_history = self.__update_chat_history.execute(
                chat_id=event.chat_id,
                new_message=message
            )

            if not event.turn_complete:
                llm_event_data = {
                    "chat_id": event.chat_id,
                    "company_id": event.company_id,
                    "chat_history": chat_history
                }

                event.event_data = llm_event_data
                
                logger.debug(f"Publishing to {event.agent_id}.process ::: {event}")
                self.___producer.publish(
                    routing_key=f"{event.agent_id}.process",
                    event_message=event
                )
        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.___producer,
                server_error=True
            )





