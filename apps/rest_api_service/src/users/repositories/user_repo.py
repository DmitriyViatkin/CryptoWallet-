from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.users import User
from .base_repo import BaseRepository

class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_active_users(self) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.is_active == True)
        )
        return list(result.scalars().all())

"""
    async def get_by_wallet_address(self, wallet_address: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.wallet_address == wallet_address)
        )
        return result.scalar_one_or_none()
"""