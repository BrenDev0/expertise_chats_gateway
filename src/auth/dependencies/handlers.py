import logging
from expertise_chats.dependencies.container import Container
from  expertise_chats.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.producers import get_producer
from src.auth.events.handlers.validate_bearer import AuthHandler
from src.auth.dependencies.use_cases import get_validate_credentials_use_case, get_validate_token_use_case
logger = logging.getLogger(__name__)

def get_auth_handler() -> AuthHandler:
    try: 
        instance_key = "auth_handler"
        handler = Container.resolve(instance_key)

    except DependencyNotRegistered:
        handler = AuthHandler(
            producer=get_producer(),
            validate_credentials=get_validate_credentials_use_case(),
            validate_token=get_validate_token_use_case()
        )

        Container.register(instance_key, handler)
        logger.info(f"{instance_key} registered")

    return handler