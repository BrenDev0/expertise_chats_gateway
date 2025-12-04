import logging
from openai import OpenAI
from typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, InteractionEvent, Producer
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.schemas.chats import GenerateChatTitle
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.errors.error_handler import handle_error

logger = logging.getLogger(__name__)


class GenerateChatTitleHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        repository: DataRepository,
        producer: Producer
    ):
        self.__repository = repository
        self.__producer = producer
        self.__client = OpenAI()

    async def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Generate chat title handler received request ::: {payload}")

        try: 
            event = InteractionEvent(**payload)
            event_data = GenerateChatTitle(**event.event_data)
            


        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.__producer,
                server_error=True
            )