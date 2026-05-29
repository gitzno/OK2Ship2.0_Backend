from abc import ABC,  abstractmethod

from src.domain.user import User


class UserRepositoryPort(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> User :
        """
        Tìm kiếm username trong database
        :param username: account do người dùng nhập vào
        :return: Trả về thông tin user của người dùng
        """
        pass
