from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.models.generated_models import Users
from domain.schemas.user_dto import LoginResponse


class UserRepository(IUserRepository):

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_user_by_account(self, account: str) -> Optional[Users]:
        """
        Triển khai logic truy vấn CSDL SQL Server
        :param account:
        :return:
        """
        async with self.session_factory() as session:
            statement = select(Users).filter(Users.Username == account)

            # 2. Thực thi truy vấn trên biến 'session' vừa được tạo ra
            result = await session.execute(statement)

            return result.scalars().first()