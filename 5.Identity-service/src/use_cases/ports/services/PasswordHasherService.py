from abc import ABC, abstractmethod


class PasswordHasherPort(ABC):

    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Băm mật khẩu thành chuỗi ký tự an toàn"""
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Kiểm tra mật khẩu raw với mật khẩu an toàn"""
        pass