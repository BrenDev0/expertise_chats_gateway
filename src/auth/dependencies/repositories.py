import logging
from src.shared.dependencies.container import Container
from src.shared.domain.exceptions.dependencies import DependencyNotRegistered
from src.shared.domain.repositories.data_repository import DataRepository
from src.auth.infrastructure.sqlAlchemy.companies_repository import SqlAlchemyCompaniesRepsoitory
logger = logging.getLogger(__name__)

def get_companies_repository() -> DataRepository:
    try:
        instance_key = "companies_repository"
        repository = Container.resolve(instance_key)

    except DependencyNotRegistered:
        repository = SqlAlchemyCompaniesRepsoitory()
        Container.register(instance_key, repository)
        logger.info(f"{instance_key} registered")
    
    return repository
