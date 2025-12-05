import logging
from expertise_chats.dependencies.container import Container
from expertise_chats.exceptions.dependencies import DependencyNotRegistered

from src.streaming.events.handlers.audio_streaming import AudioStreamingHandler
from src.streaming.events.handlers.general_streaming import GeneralStreamingHandler
from src.streaming.dependencies.services import get_tts_service
logger = logging.getLogger(__name__)

def get_audio_streaming_handler() -> AudioStreamingHandler:
    try: 
        instance_key = "audio_streaming_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = AudioStreamingHandler(
            tts_service=get_tts_service()
        )

        Container.register(instance_key, handler)

    return handler


def get_general_streaming_handler() -> GeneralStreamingHandler:
    try: 
        instance_key = "general_streaming_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = GeneralStreamingHandler()

        Container.register(instance_key, handler)

    return handler

