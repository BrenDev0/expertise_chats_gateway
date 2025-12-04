import logging
from dotenv import load_dotenv
load_dotenv()
import uvicorn
from src.app.interface.fastapi.server import create_fastapi_app
from src.app.setup.startup import startup_event

startup_event ()
logger = logging.getLogger(__name__)
app = create_fastapi_app()
logger.debug("LOGGER LEVEL SET TO DEBUG")

if __name__ == "__main__":
    uvicorn.run(
        "src.app.main:app",
        host="0.0.0.0",
        port=8000
    )
    
    