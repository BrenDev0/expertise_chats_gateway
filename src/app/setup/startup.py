import logging
from src.app.setup.broker import initialize_broker

def startup_event():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(name)s - %(message)s"
    )

    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("pika").setLevel(logging.WARNING)


    initialize_broker()