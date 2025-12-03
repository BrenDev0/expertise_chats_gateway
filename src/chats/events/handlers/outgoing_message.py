from typing import Dict, Any
from expertise_chats.broker import InteractionEvent, EventHandlerBase, Producer
from src.chats.application.use_cases.create_message import CreateMessage
from src.chats.domain.schemas.messages import OutgoingMessage

class OutgoingMessageHandler(EventHandlerBase):
    def __init__(
        self,
        create_message: CreateMessage,
        producer: Producer
    ):
        self.__create_message = create_message
        self.__producer = producer

    async def handle(self, payload: Dict[str, Any]):
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

        ## update chat history
        self.__producer.publish(
            routing_key="sessions.chat_history.update",
            event_message=event
        )
