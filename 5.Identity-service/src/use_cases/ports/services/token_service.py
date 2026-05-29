from abc import ABC, abstractmethod
from typing import Dict, Any


class TokenServicePort(ABC):

    @abstractmethod
    def generate_access_token(self, data: Dict[str, Any], expires_delta_minutes: int = None) -> str:
        """
        Nhận vào một Dictionary dữ liệu (Claims) và trả về một chuỗi JWT Token mã hóa.
        """
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Giải mã chuỗi Token và trả về thông tin Payload gốc dạng Dictionary.
        Ném ra lỗi nếu Token hết hạn hoặc không hợp lệ.
        """
        pass