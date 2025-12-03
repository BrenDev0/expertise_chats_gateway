from  typing import Dict, Any
from expertise_chats.broker import EventHandlerBase, InteractionEvent
from src.chats.application.use_cases.update_chat_history import UpdateChatHistory
from expertise_chats.broker import Producer
from src.chats.domain.entities.message import Message
class UpdateChatHistoryHandler(EventHandlerBase):
    def __init__(
        self,
        producer: Producer,
        update_chat_history: UpdateChatHistory
    ):
        self.___producer = producer
        self.__update_chat_history = update_chat_history

    def handle(self, payload: Dict[str, Any]):
        event = InteractionEvent(**payload)
        message = Message(**event.event_data)

        chat_history = self.__update_chat_history.execute(
            chat_id=event.chat_id,
            new_message=message
        )

        llm_event_data = {
            "chat_id": event.chat_id,
            "company_id": event.company_id,
            "chat_history": chat_history
        }

        event.event_data = llm_event_data
        
        self.___producer.publish(
            routing_key=f"llm.incomming.{event.agent_id}",
            event_message=event
        )





