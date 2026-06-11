from abc import ABC, abstractmethod

from domain.schemas.service_result import ServiceResult


class IRoleRepository(ABC):
    @abstractmethod
    async def set_role(self, userID: int, roleID: int, isRemove: bool = False) -> int:
        """
        set quyền cho một userID Chỉ có
        :param userID:
        :param roleID:
        :param isRemove:
        :return:
        """
        pass

