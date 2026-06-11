from uuid import UUID

from core.UnitOfWork import UnitOfWork
from domain.interfaces.services.i_user_service import IUserService
from domain.models import generated_models
from domain.schemas.service_result import ServiceResult
from domain.schemas.user_dto import UserResponse


class UserService(IUserService):
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def get_user_by_id(self, user_id: UUID) -> ServiceResult[generated_models.Users]:
        pass

    def update_user_by_id(self, user_id: UUID) -> ServiceResult[UserResponse]:
        pass

    def get_users(self) -> ServiceResult[UserResponse]:
        pass