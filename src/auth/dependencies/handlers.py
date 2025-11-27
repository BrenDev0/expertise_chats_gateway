import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.producers import get_producer
from src.auth.events.handlers.token_validation import AuthHandler
logger = logging.getLogger(__name__)

def get_auth_handler() -> AuthHandler:
    try: 
        instance_key = "auth_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = AuthHandler(
            producer=get_producer()
        )

        Container.register(instance_key, handler)

    return handler