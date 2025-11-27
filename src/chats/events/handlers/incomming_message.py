from  typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, BaseEvent
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.chats.application.use_cases.create_message import CreateMessage
from expertise_chats.broker import Producer
from src.shared.domain.schemas.ws_responses import WsPayload

class IncommingMessageHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        create_message: CreateMessage,
        producer: Producer
    ):
        self.__create_message = create_message
        self.__producer = producer

    async def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
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

        message_saved_event = BaseEvent(
            chat_id=event.chat_id,
            user_id=event.user_id,
            event_data= ws_payload.model_dump()
        )

        ## send message data to front
        self.__producer.publish(
            routing_key="streaming.general.outbound.send",
            event_message=message_saved_event
        )

        ## send to session consumer
        



