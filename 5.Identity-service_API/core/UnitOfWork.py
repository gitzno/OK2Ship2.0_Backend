from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from infrastructures.database.repositories.user_repository import UserRepository


class UnitOfWork:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self._session_factory = session_factory
        self.session: AsyncSession = None

    async def __aenter__(self):
        self.session = self._session_factory()

        self.users = UserRepository(self.session)

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                # Nếu trong khối lệnh `async with` xảy ra bất kỳ lỗi gì, tự động Rollback
                await self.rollback()
            else:
                # Nếu chạy mượt mà không lỗi, tự động Commit toàn bộ các Repo cùng một lúc
                await self.commit()
        finally:
            await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()