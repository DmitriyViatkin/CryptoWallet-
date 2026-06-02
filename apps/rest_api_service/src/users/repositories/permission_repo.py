from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.permissions import Permission
from src.users.repositories.base_repo import BaseRepository

class PermissionRepository(BaseRepository[Permission]):

    def __init__(self, session: AsyncSession):
        super().__init__(Permission, session)

    async def get_by_user_id(self, user_id: int) -> Permission | None:
        result = await self.session.execute(
            select(Permission).where(Permission.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def set_chat_access(self, user_id: int, has_access: bool) -> Permission | None:
        permission = await self.get_by_user_id(user_id)
        if not permission:
            return None
        return await self.update(permission, has_chat_access=has_access)
