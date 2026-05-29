from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List
from uuid import UUID


T = TypeVar('T')

class BaseRepositoryPort(ABC, Generic[T]):

    @abstractmethod
    def get_by_field(self, field: list[str], value: list[str]) -> List[T]:
        """Tìm kiếm đữ liệu theo trường"""
        pass

    @abstractmethod
    def get_by_id(self, id: UUID) -> Optional[T]:
        """Tìm kiếm một bản ghi theo ID duy nhất"""
        pass

    @abstractmethod
    def delete_by_id(self, id: UUID) -> Optional[T]:
        """Xóa bản ghi theo ID"""
        pass
