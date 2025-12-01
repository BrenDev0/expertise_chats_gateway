import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.dependencies.producers import get_producer
from src.auth.application.use_cases.validate_credentials import ValidateCredentials
from src.auth.application.use_cases.validate_token import ValidateToken
from src.auth.dependencies.repositories import get_companies_repository
logger = logging.getLogger(__name__)

def get_validate_token_use_case() -> ValidateToken:
    try: 
        instance_key = "validate_token_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = ValidateToken()

        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case

def get_validate_credentials_use_case() -> ValidateCredentials:
    try: 
        instance_key = "validate_credentials_use_case"
        use_case = Container.resolve(instance_key)

    except DependencyNotRegistered:
        use_case = ValidateCredentials(
            repository=get_companies_repository()
        )

        Container.register(instance_key, use_case)
        logger.info(f"{instance_key} registered")

    return use_case



