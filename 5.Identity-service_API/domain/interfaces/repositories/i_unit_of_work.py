from abc import ABC, abstractmethod
from typing import Any

from domain.interfaces.repositories.i_role_repository import IRoleRepository
from domain.interfaces.repositories.i_user_repository import IUserRepository


class IUnitOfWork(ABC):
    """
    Interface định nghĩa hợp đồng cho Unit of Work.
    """
    

    users: IUserRepository
    roles: IRoleRepository


    @abstractmethod
    async def __aenter__(self) -> 'IUnitOfWork':
        """Khởi tạo context và trả về chính IUnitOfWork"""
        pass


    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Xử lý dọn dẹp, commit hoặc rollback khi thoát khỏi khối async with"""
        pass


    @abstractmethod
    async def commit(self) -> None:
        """Lưu các thay đổi xuống Database"""
        pass


    @abstractmethod
    async def rollback(self) -> None:
        """Hoàn tác các thay đổi nếu có lỗi"""
        pass