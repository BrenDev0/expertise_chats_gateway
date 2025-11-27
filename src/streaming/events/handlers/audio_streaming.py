import logging
from typing import Any, Dict
from expertise_chats.broker import AsyncEventHandlerBase, BaseEvent

from src.streaming.domain.services.text_to_speech import TextToSpeech
from src.streaming.events.schemas import LlmChunk
from src.shared.utils.ws_connections import WebsocketConnectionsContainer
from src.streaming.utils.decorators.streaming_error_handler import streaming_error_hanlder
from src.shared.domain.schemas.ws_responses import WsPayload
logger = logging.getLogger(__name__)

class AudioStreamingHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        tts_service: TextToSpeech
    ):
        self.__tts_service = tts_service

    @streaming_error_hanlder(module="streaming.auido.outbound.handler")
    async def handle(self, payload: Dict[str, Any]):
        event = BaseEvent(**payload)
        chunk = LlmChunk(**event.event_data)
        
        ws = WebsocketConnectionsContainer.resolve_connection(event.chat_id)
        if not ws:
            return 
        
        audio_chunk = self.__tts_service.transcribe(chunk.chunk)
        ws_payload = WsPayload(
            type="AUDIO",
            data=audio_chunk
        )

        await ws.send_json(ws_payload.model_dump())

        

    





