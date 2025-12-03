from fastapi import FastAPI
from contextlib import asynccontextmanager
from  uuid import UUID
from src.shared.dependencies.container import Container

from src.app.setup.startup import startup_event
from src.interactions.interface.fastapi import interactions_ws
from src.shared.utils.ws_connections import WebsocketConnectionsContainer

def create_fastapi_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        startup_event()
        yield
    
    app = FastAPI(lifespan=lifespan)

    @app.get("/health", tags=["Internal"])
    async def health():
        """
        ## Health check 
        This endpoints verifies server status.
        """
        return {"status": "ok"}

    @app.get("/connections", tags=["Internal"])
    async def get_websocket_connections():
        connections = WebsocketConnectionsContainer._active_connections

        return {
            "connection_ids": list(connections.keys()),
            "count": len(connections)
        }

    @app.delete("/connections/{connection_id}", tags=["Internal"])
    async def get_websocket_connections(
        connection_id: UUID
    ):
        WebsocketConnectionsContainer.remove_connection(connection_id=connection_id)

        connections = WebsocketConnectionsContainer._active_connections

        return {
            "connection_ids": list(connections.keys()),
            "count": len(connections)
        }


    @app.get("/instances", tags=["Internal"])
    async def instances():
        """
        ## Gets instances registered in the dependencies ccontainer
        """
        return Container.get_instances()

    app.include_router(interactions_ws.router)

    return app