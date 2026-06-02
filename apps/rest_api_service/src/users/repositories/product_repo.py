from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.product import Product
from src.users.repositories.base_repo import BaseRepository


class ProductRepository(BaseRepository[Product]):

    def __init__(self, session: AsyncSession):
        super().__init__(Product, session)

    async def get_by_user_id(self, user_id: int) -> list[Product]:
        result = await self.session.execute(
            select(Product).where(Product.user_id == user_id)
        )
        return list(result.scalars().all())