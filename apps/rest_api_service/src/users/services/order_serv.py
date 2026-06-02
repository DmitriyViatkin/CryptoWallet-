from decimal import Decimal
from src.users.models.orders import Order
from src.users.models.order_items import OrderItems
from src.users.repositories.order_repo import OrderRepository
from src.users.repositories.product_repo import ProductRepository
from src.users.services.base_service import BaseService


class OrderService(BaseService[Order]):
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
    ) -> None:
        super().__init__(order_repo)
        self._order_repo = order_repo
        self._product_repo = product_repo

    # ── Order ─────────────────────────────────────────────────────────────────

    async def create_order(
        self, buyer_id: int, items: list[dict]
    ) -> Order:
        """
        Створення замовлення разом з айтемами (одна транзакція).
        items = [{"product_id": int, "quantity": int}, ...]

        Логіка:
        - Завантажити кожен Product, перевірити існування
        - Зафіксувати ціну на момент замовлення (product.price)
        - Підрахувати amount = sum(price * quantity)
        - Створити Order (статус PENDING, tx_hash=None)
        - Створити OrderItems записи з фіксованою ціною
        - Все в одній сесії (session вже shared через репозиторій)
        """
        raise NotImplementedError

    async def confirm_payment(self, order_id: int, tx_hash: str) -> Order | None:
        """
        Підтвердження оплати покупцем.
        - Перевірка order існує і статус == PENDING
        - tx_hash унікальний (немає іншого замовлення з таким хешем)
        - Оновлення: tx_hash + статус → DELIVERY
        """
        order = await self._order_repo.get_by_id(order_id)
        if not order:
            return None
        raise NotImplementedError

    async def complete_order(self, order_id: int) -> Order | None:
        """
        Завершення доставки — викликається TaskIQ воркером.
        - Перевірка статус == DELIVERY
        - Статус → COMPLETED
        """
        order = await self._order_repo.get_by_id(order_id)
        if not order:
            return None
        raise NotImplementedError

    async def cancel_order(self, order_id: int, buyer_id: int) -> Order | None:
        """
        Скасування замовлення покупцем.
        - Перевірка order.buyer_id == buyer_id (тільки свої)
        - Дозволено тільки зі статусу PENDING
        - Статус → CANCELLED
        """
        order = await self._order_repo.get_by_id(order_id)
        if not order or order.buyer_id != buyer_id:
            return None
        raise NotImplementedError

    async def get_user_orders(self, user_id: int) -> list[Order]:
        """Замовлення юзера з items (selectinload вже в репо)."""
        return await self._order_repo.get_by_user_id(user_id)

    async def get_oldest_in_delivery(self) -> Order | None:
        """Для TaskIQ воркера — наступне замовлення на доставку."""
        return await self._order_repo.get_oldest_in_delivery()

    # ── OrderItems (читання) ──────────────────────────────────────────────────

    async def get_order_with_items(self, order_id: int, buyer_id: int) -> Order | None:
        """
        Замовлення з айтемами для конкретного юзера.
        - get_by_id повертає Order без items (немає selectinload)
        - Тому беремо через get_by_user_id і фільтруємо
          (або додати окремий метод в репо з selectinload по id)
        """
        orders = await self._order_repo.get_by_user_id(buyer_id)
        return next((o for o in orders if o.id == order_id), None)