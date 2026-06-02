from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.wallet_operations import WalletOperation
from src.users.repositories.base_repo import BaseRepository


class WalletOperationRepository(BaseRepository[WalletOperation]):

    def __init__(self, session: AsyncSession):
        super().__init__(WalletOperation, session)

    async def get_by_wallet_id(self, wallet_id: int) -> list[WalletOperation]:
        result = await self.session.execute(
            select(WalletOperation).where(WalletOperation.wallet_id == wallet_id)
        )
        return list(result.scalars().all())

    async def get_by_tx_hash(self, tx_hash: str) -> WalletOperation | None:
        result = await self.session.execute(
            select(WalletOperation).where(WalletOperation.tx_hash == tx_hash)
        )
        return result.scalar_one_or_none()