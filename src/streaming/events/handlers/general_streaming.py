import logging
from typing import Any, Dict
from expertise_chats.broker import AsyncEventHandlerBase, BaseEvent

from src.shared.utils.ws_connections import WebsocketConnectionsContainer
from src.shared.domain.schemas.ws_responses import WsPayload
from src.streaming.utils.decorators.streaming_error_handler import streaming_error_hanlder
logger = logging.getLogger(__name__)

class GeneralStreamingHandler(AsyncEventHandlerBase):
    @streaming_error_hanlder(module="streaming.auido.outbound.handler")
    async def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
        ws_payload = WsPayload(**event.event_data)
        
        ws = WebsocketConnectionsContainer.resolve_connection(event.chat_id)
        if not ws:
            return 
        
        await ws.send_json(ws_payload.model_dump())

        

    





