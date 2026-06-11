from sqlalchemy import delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from domain.interfaces.repositories.i_role_repository import IRoleRepository
from domain.models import generated_models


class RoleRepository(IRoleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def set_role(self, user_id: int, role_id: int, is_remove: bool = False) -> bool:
        # Lưu ý: Tên cột lấy theo file SQL của bạn là UserIDI và RoleID

        if is_remove:
            # XÓA QUYỀN
            stmt = delete(generated_models.t_UserRoles).where(
                generated_models.t_UserRoles.c.UserIDI == user_id,
                generated_models.t_UserRoles.c.RoleID == role_id
            )
            await self.session.execute(stmt)
        else:
            try:
                # THÊM QUYỀN
                stmt = insert(generated_models.t_UserRoles).values(
                    UserIDI=user_id,
                    RoleID=role_id
                )
                await self.session.execute(stmt)
            except Exception as e:
                print(e)
        return True
