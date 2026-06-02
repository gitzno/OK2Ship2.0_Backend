from abc import abstractmethod, ABC
from typing import Any, Dict


class ITokenService(ABC):

    @abstractmethod
    def generate_access_token(self, data: Dict[str, Any], expires_delta_minutes: Optional[int] = None) -> str:
        """
        Tạo mã JWT Access Token dựa trên dữ liệu đầu vào.

        Args:
            data (Dict[str, Any]): Dữ liệu payload muốn nhúng vào token (vd: user_id, username).
            expires_delta_minutes (int, optional): Thời gian sống của token (tính bằng phút).
                                                   Nếu không truyền, sẽ lấy mặc định từ config.

        Returns:
            str: Chuỗi JWT token đã được ký.
        """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Giải mã và xác thực JWT Access Token.

        Args:
            token (str): Chuỗi JWT cần giải mã.

        Returns:
            Dict[str, Any]: Dữ liệu payload bên trong token nếu hợp lệ.

        Raises:
            TokenExpiredError: Nếu token đã quá hạn.
            TokenInvalidError: Nếu chữ ký không đúng hoặc cấu trúc token bị sai.
        """
        pass
