from abc import ABC, abstractmethod
from domain.schemas.user_dto import LoginRequest


class IAuthService(ABC):

    @abstractmethod
    async def login(self, request: LoginRequest) -> str:
        """
        Xử lý nghiệp vụ đăng nhập của người dùng.

        Args:
            request (LoginRequest): Dữ liệu yêu cầu đăng nhập chứa tài khoản và mật khẩu.

        Returns:
            str: Chuỗi Access Token (JWT) nếu đăng nhập thành công.

        Raises:
            Exception: Nếu tài khoản không tồn tại.
            AccountNotFoundError: Nếu trạng thái tài khoản không hợp lệ.
            PasswordIncorrectError: Nếu sai mật khẩu.
        """
        pass