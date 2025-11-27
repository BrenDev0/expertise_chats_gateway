from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.app.setup.startup import startup_event
from src.interactions.interface.fastapi import interactions_ws

def create_fastapi_app():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        startup_event()
        yield
    
    app = FastAPI(lifespan=lifespan)

    app.include_router(interactions_ws.router)

    return app