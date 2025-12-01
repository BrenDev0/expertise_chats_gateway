from fastapi import APIRouter, Depends, Body, Request, UploadFile, File
from fastapi.security import HTTPBearer
from typing import List
from uuid import UUID
from src.app.interface.fastapi.middleware.hmac import verify_hmac
from src.chats.domain.schemas.chats import ChatPublic, ChatUpdate, ChatCreate
from src.shared.domain.schemas.http_responses import CommonHttpResponse


security = HTTPBearer()
router = APIRouter(
    prefix="/chats",
    tags=["Chats"],
    dependencies=[Depends(security), Depends(verify_hmac)] 
)

@router.post("/secure/create", status_code=201, response_model=ChatPublic)
def secure_create(
    req: Request,
    data: ChatCreate = Body(...)
):
    """
    ## Chat create request

    This endpoint creates a chat in the database.
    The id returned is needed for all interactions requests.
    """
    pass

@router.post("/secure/context/{chat_id}", status_code=201, response_model=CommonHttpResponse)
async def secure_add_chat_context(
    chat_id: UUID,
    req: Request,
    file: UploadFile = File(...)
): 
    """
    ## Add context to chat

    This endpoint will add a tempory source of context for the agent that will last one request
    """
    pass

@router.get("/secure/collection", status_code=200, response_model=List[ChatPublic])
def secure_collection( 
    req: Request
):
    """
    ## Chat collection request

    This endpoint returns a list of chats by the user id in the auth token.
    """
    pass


@router.patch("/secure/{chat_id}", status_code=200, response_model=CommonHttpResponse)
def secure_update(
    chat_id: UUID,
    req: Request,
    data: ChatUpdate
): 
    """
    ## Update request

    This endpont updates the title of the chat provided in the params
    """
    pass

@router.delete("/secure/{chat_id}", status_code=200, response_model=CommonHttpResponse)
def secure_delete(
    chat_id: UUID,
    req: Request
):
    """
    ## Delete request 

    This endpoint deletes a chat by id.
    """
    pass

@router.delete("/secure/context/{chat_id}/{filename}", status_code=200, response_model=CommonHttpResponse)
def secure_remove_chat_context(
    chat_id: UUID,
    filename: str,
    req: Request
):
    """
    ## Remove context from chat

    This endpoint will remove the file noted in the params from the vecotr base
    """
    pass
    