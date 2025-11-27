from  typing import Dict, Any
from expertise_chats.broker import EventHandlerBase, BaseEvent
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.chats.application.use_cases.create_message import CreateMessage
from expertise_chats.broker import Producer
from src.shared.domain.schemas.ws_responses import WsPayload

class UpdateChatHistoryHandler(EventHandlerBase):
    def __init__(
        self,
        producer: Producer
    ):
        self.___producer = producer

    def handle(self, payload):
        pass