import logging
from typing import Any, Dict, Union
from expertise_chats.broker import AsyncEventHandlerBase, InteractionEvent, BaseEvent
from expertise_chats.schemas.ws import WsPayload
from src.streaming.domain.services.text_to_speech import TextToSpeech
from src.shared.utils.ws_connections import WebsocketConnectionsContainer
from src.streaming.utils.decorators.streaming_error_handler import streaming_error_hanlder

logger = logging.getLogger(__name__)

class AudioStreamingHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        tts_service: TextToSpeech
    ):
        self.__tts_service = tts_service

    async def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Streaming Audio handler received request ::: {payload}")
        
        event = InteractionEvent(**payload)
        ws_payload = WsPayload(**event.event_data)
        
        ws = WebsocketConnectionsContainer.resolve_connection(event.chat_id)
        if not ws:
            return 
        
        audio_chunk = self.__tts_service.transcribe(ws_payload.data)
        ws_payload.data = audio_chunk
       
        logger.debug(f"Streaming  Audio Sending ::: {ws_payload.model_dump()}")
        
        try:
            await ws.send_json(ws_payload.model_dump())
        except Exception as e:
                if "closed" in str(e).lower() or "disconnect" in str(e).lower():
                    logger.info(f"Connection {event.chat_id} disconnected")
                    return
                
                logger.error(f"Connection id: {event.chat_id} ::::, Error sending data :::: {e}")
                raise e
        

    





