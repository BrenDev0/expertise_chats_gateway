import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from  src.streaming.domain.services.text_to_speech import TextToSpeech
from src.streaming.infrastructure.deepgram.text_to_speech import DeepgramTextToSpeechService
logger = logging.getLogger(__name__)

def get_tts_service() -> TextToSpeech:
    try:
        instance_key = "tts_service"
        service = Container.resolve(instance_key)

    except DependencyNotRegistered:
        service = DeepgramTextToSpeechService()

        Container.register(instance_key, service)
        logger.info(f"{instance_key} registered")
    
    return service

