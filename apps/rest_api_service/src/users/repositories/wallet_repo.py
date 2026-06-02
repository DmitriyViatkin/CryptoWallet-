from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.wallets import Wallet
from src.users.repositories.base_repo import BaseRepository

class WalletRepository(BaseRepository[Wallet]):

    def __init__(self, session: AsyncSession):
        super().__init__(Wallet, session)

    async def get_by_address(self, address: str) -> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(Wallet.address == address)
        )
        return result.scalar_one_or_none()
    async def get_by_address_and_user(self,address: str, user_id: int)-> Wallet | None:
        result = await self.session.execute(
            select(Wallet).where(Wallet.address == address, Wallet.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: int) -> list[Wallet]:
        result = await self.session.execute(
        select(Wallet).where(Wallet.user_id == user_id)
        )
        return result.scalars().all()
