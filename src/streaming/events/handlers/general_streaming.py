import logging
from typing import Any, Dict, Union
from expertise_chats.broker import AsyncEventHandlerBase, InteractionEvent
from expertise_chats.schemas.ws import WsPayload
from src.shared.utils.ws_connections import WebsocketConnectionsContainer
logger = logging.getLogger(__name__)

class GeneralStreamingHandler(AsyncEventHandlerBase):
    async def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Streaming General handler received request ::: {payload}")
        
        event = InteractionEvent(**payload)
        ws_payload = WsPayload(**event.event_data)
        
        ws = WebsocketConnectionsContainer.resolve_connection(event.chat_id)
        if not ws:
            return 
        
        logger.debug(f"Streaming  General Sending ::: {ws_payload.model_dump()}")
        try:
            await ws.send_json(ws_payload.model_dump())
        
        except Exception as e:
                if "closed" in str(e).lower() or "disconnect" in str(e).lower():
                    logger.info(f"Connection {event.chat_id} disconnected")
                    return
                
                logger.error(f"Connection id: {event.chat_id} ::::, Error sending data :::: {e}")
                return 
        

    





