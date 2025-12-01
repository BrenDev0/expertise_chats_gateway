import logging
from typing import Union
from uuid import UUID
from src.auth.domain.entities import Company
from src.auth.domain.schemas import AuthError
from src.shared.domain.repositories.data_repository import DataRepository
logger = logging.getLogger(__name__)

class ValidateCredentials:
    def __init__(
        self,
        repository: DataRepository
    ):
        self.__repository = repository

    def execute(
        self,
        company_id: Union[UUID, str],
        user_id: Union[UUID, str]
    ):
        company: Company = self.__repository.get_one(key="compay_id", value=company_id)

        if not Company:
            raise AuthError(
                error="Authorization Error",
                detail="No valid company id found in token",
            )

        if str(company.user_id) != str(user_id):
            logger.warning(f"resource_id ::: {company_id} ::: resource ::: {company.model_dump()} ::: user ::: {user_id}")
            raise AuthError(
                error="Authorization Error",
                detail="Forbidden",
                additional_info="User does not have access to requested data"
            )
        
        
        


