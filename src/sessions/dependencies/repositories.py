import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered

from src.sessions.domain.repositories.sessions_repository import SessionRepository
from src.sessions.infrastructure.redis.session_repository import RedisSessionRepository
logger = logging.getLogger(__name__)

def get_sessions_repository() -> SessionRepository:
    try:
        instance_key = "sessions_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = RedisSessionRepository()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")
    
    return repository
