from abc import abstractmethod, ABC
from typing import Optional

from domain.models.generated_models import Users
from domain.schemas.user_dto import LoginResponse


class IUserRepository(ABC):

    @abstractmethod
    async def get_user_by_account(self, account: str) -> Optional[Users]:
        """
        Tìm kiếm thông tin người dùng dựa trên tên tài khoản.

        Args:
            account (str): Tên đăng nhập hoặc email của người dùng.

        Returns:
            Optional[UserModel]: Trả về đối tượng Model người dùng nếu tìm thấy, ngược lại trả về None.
        """
        pass

