import re
from decimal import Decimal, InvalidOperation

from src.users.models import Product
from src.users.models.product import Product
from src.users.repositories.product_repo import ProductRepository
from src.users.services.base_service import BaseService
from src.exception.product_except import (ProductAlreadyExistsError,
    InvalidWalletAddressError, ProductNotFoundError, ProductAccessDeniedError,
    InvalidPriceError)

class ProductService(BaseService[Product]):
    def __init__(self, product_repo: ProductRepository) -> None:
        super().__init__(product_repo)
        self._product_repo = product_repo

    async def create_product(
        self,
        user_id: int,
        title: str,
        wallet_address: str,
        price: Decimal,  # Decimal-сумісний рядок
    ) -> Product:
        """
        Створення продукту.
        - Валідація price > 0
        - Валідація wallet_address (формат EVM адреси)
        - Збереження в БД
        """
        clean_title = title.strip() if title else ""
        if not clean_title:
            raise ValueError(
                "Название продукта не может быть пустым или состоять из одних пробелов.")
        if len(clean_title) > 100:
            raise ValueError("Название продукта не может быть длиннее 100 символов.")

        # 2. Валидация цены (price > 0)
        try:
            # Пытаемся преобразовать строку в Decimal
            decimal_price = Decimal(price)
        except (InvalidOperation, TypeError):
            raise InvalidPriceError(
                f"Некорректный формат цены: '{price}'. Ожидалось числовое значение.")

        if decimal_price <= 0:
            raise InvalidPriceError("Цена продукта должна быть строго больше нуля.")

        # 3. Валидация wallet_address (Строгий формат EVM кошелька)
        # Начинается с 0x, за которым следует ровно 40 шестнадцатеричных символов (0-9, a-f)
        evm_pattern = r"^0x[a-fA-F0-9]{40}$"
        if not wallet_address or not re.match(evm_pattern, wallet_address):
            raise InvalidWalletAddressError(
                f"Некорректный EVM-адрес кошелька: '{wallet_address}'. "
                f"Адрес должен начинаться с 0x и содержать ровно 42 символа."
            )

        # 4. Сохранение в базу данных через репозиторий
        # Базовый репозиторий примет именованные аргументы (**kwargs)
        return await self._product_repo.create(
            user_id=user_id,
            title=clean_title,
            wallet_address=wallet_address,
            price=decimal_price  # В БД улетает уже валидный объект Decimal
        )

    async def get_user_products(self, user_id: int) -> list[Product]:
        return await self._product_repo.get_by_user_id(user_id)

    async def update_product(
            self,
            product_id: int,
            user_id: int,
            **kwargs
    ) -> Product | None:
        """
        Оновлення продукту.
        - Перевірка що product.user_id == user_id (тільки власник)
        - Якщо оновлюється price — валідація > 0
        """
        product = await self._product_repo.get_by_id(product_id)
        if not product :
            raise ProductNotFoundError("Продукт не найден.")
        if product.user_id != user_id:
            raise ProductAccessDeniedError("У пользователя нет прав на редактирование этого продукта.")
        if "title" in kwargs:
            title = kwargs["title"]

            clean_title = title.strip() if title else ""
            if not clean_title:
                raise ValueError(
                    "Название продукта не может быть пустым или состоять из одних пробелов.")
            if len(clean_title) > 100:
                raise ValueError("Название продукта не может быть длиннее 100 символов.")

        # 2. Валидация цены (price > 0)
        if "price" in kwargs:
            price = kwargs["price"]
            try:
                # Пытаемся преобразовать строку в Decimal
                decimal_price = Decimal(price)
            except (InvalidOperation, TypeError):
                raise InvalidPriceError(
                    f"Некорректный формат цены: '{price}'. Ожидалось числовое значение.")

            if decimal_price <= 0:
                raise InvalidPriceError("Цена продукта должна быть строго больше нуля.")

        # 3. Валидация wallet_address (Строгий формат EVM кошелька)
        # Начинается с 0x, за которым следует ровно 40 шестнадцатеричных символов (0-9, a-f)
        if "wallet_address" in kwargs:
            wallet_address = kwargs["wallet_address"]
            evm_pattern = r"^0x[a-fA-F0-9]{40}$"
            if not wallet_address or not re.match(evm_pattern, wallet_address):
                raise InvalidWalletAddressError(
                    f"Некорректный EVM-адрес кошелька: '{wallet_address}'. "
                    f"Адрес должен начинаться с 0x и содержать ровно 42 символа."
                )

        # 4. Сохранение в базу данных через репозиторий
        # Базовый репозиторий примет именованные аргументы (**kwargs)
        return await self._product_repo.update(
            instance=product,
             **kwargs
        )

    async def delete_product(self, product_id: int, user_id: int) -> bool:
        """
        Видалення продукту.
        - Перевірка що product.user_id == owner_id
        - Перевірка що продукт не використовується в активних замовленнях
          (OrderItems → Order зі статусом PENDING/DELIVERY)
        - Повертає True якщо видалено, False якщо не знайдено або не власник
        """
        product = await self._product_repo.get_by_id(product_id)
        if not product :
            raise ProductNotFoundError("Продукт не найден.")

        if product.user_id !=  user_id:
            raise ProductAccessDeniedError(
                "У пользователя нет прав на удаление этого продукта.")
        return await self._product_repo.delete(id=product_id)


