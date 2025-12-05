import logging
from openai import OpenAI
from typing import Dict, Any
from expertise_chats.broker import AsyncEventHandlerBase, InteractionEvent, Producer
from src.shared.domain.repositories.data_repository import DataRepository
from src.chats.domain.schemas.chats import GenerateChatTitle
from src.chats.application.use_cases.update_chat import UpdateChat
from src.chats.domain.schemas.chats import ChatUpdate
from expertise_chats.schemas.ws import WsPayload
from expertise_chats.errors.error_handler import handle_error

logger = logging.getLogger(__name__)


class GenerateChatTitleHandler(AsyncEventHandlerBase):
    def __init__(
        self,
        update_chat: UpdateChat,
        producer: Producer
    ):
        self.__update_chat = update_chat
        self.__producer = producer
        self.__client = OpenAI()

    async def handle(self, payload: Dict[str, Any]):
        logger.debug(f"Generate chat title handler received request ::: {payload}")

        try: 
            event = InteractionEvent(**payload)
            event_data = GenerateChatTitle(**event.event_data)
    
            response = self.__client.responses.create(
                model="gpt-4.0",
                input=f"""
                summerize the the users message to a short and informative chat title

                - users message:
                    {event_data.first_message}
                """
            )

            logger.debug(f"OPENAI RESPONSE ::: {response.output_text}")

            changes = ChatUpdate(
                title=response.output_text.strip()
            )

            updated_chat = self.__update_chat.execute(
                chat_id=event_data.chat_id,
                changes=changes
            )

            ws_payload = WsPayload(
                type="TITLE",
                data=updated_chat.modeldump()
            )

            event.event_data = ws_payload

            logger.debug(f"Publishing to streaming.general.outbound.send ::: {event.model_dump()}")
            self.__producer.publish(
                routing_key="streaming.general.outbound.send",
                event_message=event
            )

        except Exception as e:
            logger.error(str(e))
            handle_error(
                event=event,
                producer=self.__producer,
                server_error=True
            )