from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.models.orders import Order
from src.users.repositories.base_repo import BaseRepository


class OrderRepository(BaseRepository[Order]):

    def __init__(self, session: AsyncSession):
        super().__init__(Order, session)

    async def get_by_user_id(self, user_id: int) -> list[Order]:
        result = await self.session.execute(
            select(Order)
            .where(Order.buyer_id == user_id)
            .options(selectinload(Order.items))  # підвантажуємо items одразу
        )
        return list(result.scalars().all())

    async def get_oldest_in_delivery(self) -> Order | None:
        """Для TaskIQ обробника — береємо найстаріший зі статусом DELIVERY."""
        from apps.rest_api_service.enums import OrderStatus
        result = await self.session.execute(
            select(Order)
            .where(Order.status == OrderStatus.DELIVERY)
            .order_by(Order.created_at.asc())
            .limit(1)
        )
        return result.scalar_one_or_none()