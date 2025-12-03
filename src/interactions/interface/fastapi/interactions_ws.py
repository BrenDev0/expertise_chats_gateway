import logging
import os
from  pydantic import ValidationError
from fastapi import APIRouter, WebSocket, status, WebSocketDisconnect, Depends
from uuid import UUID
from expertise_chats.broker import Producer
from src.app.middleware.hmac.ws import verify_hmac_ws
from src.shared.utils.ws_connections import WebsocketConnectionsContainer
from src.shared.domain.schemas.ws_requests import InteractionRequest
from src.shared.domain.schemas.ws_responses import WsPayload, RequestErrorBase
from src.shared.events.schemas.interactions import InteractionEvent

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Interactions"]
)

def get_producer() -> Producer:
    exchange = os.getenv("EXCHANGE")
    return Producer(
        exchange=exchange
    )

@router.websocket("/interactions/{chat_id}")
async def websocket_interact(
    websocket: WebSocket, 
    chat_id: UUID,
    producer: Producer = Depends(get_producer)
):
    
    params = websocket.query_params
    signature = params.get("x-signature")
    payload = params.get("x-payload")

    if not await verify_hmac_ws(signature, payload):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()

    WebsocketConnectionsContainer.register_connection(chat_id, websocket)
    
    logger.info(f'Websocket connection: {chat_id} opened.')

    try:
        while True: 
            message = await websocket.receive_json()

            try:
                
                req = InteractionRequest(**message)

                event = InteractionEvent(
                    chat_id=chat_id,
                    user_id="TBD",
                    agent_id=req.agent_id,
                    event_data=req
                )

                producer.publish(
                    routing_key="auth.validation.validate",
                    event_message=event
                )
            
            except ValidationError as e:
                logger.error(f"Bad request {e.errors()}")

                error_response = RequestErrorBase(
                    error="Bad Request",
                    additional_info=InteractionRequest.model_json_schema(),
                    detail=e.errors()
                )
    
                payload = WsPayload(
                    type="ERROR",
                    data=error_response.model_dump()
                )

                await websocket.send_json(payload.model_dump())
            
            except Exception as e:
                logger.error(f"Error receiving message: {e}")
                error_response = RequestErrorBase(
                    error="Bad Request",
                    detail="Invalid JSON"
                )

                payload = WsPayload(
                    type="ERROR",
                    data=error_response.model_dump()
                )
                await websocket.send_json(payload.model_dump())

    except WebSocketDisconnect:
        WebsocketConnectionsContainer.remove_connection(chat_id)
        logger.info(f'Websocket connection: {chat_id} closed.')