import uuid
from abc import abstractmethod, ABC
from typing import Any, Dict
from uuid import UUID

from domain.schemas.service_result import ServiceResult
from domain.schemas.user_dto import UserResponse


class IUserService(ABC):
    @abstractmethod
    def get_users(self) -> ServiceResult[UserResponse]:
        """
           Lấy dữ liệu danh sách người dùng
           Returns:
               ServiceResult[UserResponse]: Danh sách người dùng
           Raises:
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: UUID) -> ServiceResult[UserResponse]:
        """
        Lấy dữ liệu người qua ID
        :param user_id:
        :return:
        """
        pass

    @abstractmethod
    def update_user_by_id(self, user_id: UUID) -> ServiceResult[UserResponse]:
        """
        Chỉnh sửa người dùng với id
        :param user_id:
        :return:
        """
        pass

