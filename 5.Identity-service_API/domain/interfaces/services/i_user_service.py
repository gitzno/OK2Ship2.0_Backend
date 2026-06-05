from abc import abstractmethod, ABC
from typing import Any, Dict

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
