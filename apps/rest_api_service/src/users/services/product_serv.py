from src.users.models.product import Product
from src.users.repositories.product_repo import ProductRepository
from src.users.services.base_service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self, product_repo: ProductRepository) -> None:
        super().__init__(product_repo)
        self._product_repo = product_repo

    async def create_product(
        self,
        user_id: int,
        title: str,
        wallet_address: str,
        price: str,  # Decimal-сумісний рядок
    ) -> Product:
        """
        Створення продукту.
        - Валідація price > 0
        - Валідація wallet_address (формат EVM адреси)
        - Збереження в БД
        """
        raise NotImplementedError

    async def get_user_products(self, user_id: int) -> list[Product]:
        return await self._product_repo.get_by_user_id(user_id)

    async def update_product(
        self, product_id: int, owner_id: int, **kwargs
    ) -> Product | None:
        """
        Оновлення продукту.
        - Перевірка що product.user_id == owner_id (тільки власник)
        - Якщо оновлюється price — валідація > 0
        """
        product = await self._product_repo.get_by_id(product_id)
        if not product or product.user_id != owner_id:
            return None
        raise NotImplementedError

    async def delete_product(self, product_id: int, owner_id: int) -> bool:
        """
        Видалення продукту.
        - Перевірка що product.user_id == owner_id
        - Перевірка що продукт не використовується в активних замовленнях
          (OrderItems → Order зі статусом PENDING/DELIVERY)
        - Повертає True якщо видалено, False якщо не знайдено або не власник
        """
        product = await self._product_repo.get_by_id(product_id)
        if not product or product.user_id != owner_id:
            return False
        raise NotImplementedError