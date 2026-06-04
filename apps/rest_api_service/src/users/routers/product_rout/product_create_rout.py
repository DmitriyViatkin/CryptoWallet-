import logging
from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject
from src.users.services.product_serv import ProductService
from src.users.schemas.product_sch.product_create_sch import ProductCreateSch
from src.users.schemas.product_sch.product_resp_sch import ProductResponseSch
from src.auth.dependencies import get_current_user
from src.exception.product_except import InvalidPriceError, InvalidWalletAddressError

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/create", response_model=ProductResponseSch,
             status_code=status.HTTP_201_CREATED)
@inject
async def create_product(
    body: ProductCreateSch,
    product_service: FromDishka[ProductService],
    current_user=Depends(get_current_user)
) -> ProductResponseSch:
    """
    Створення нового продукту для поточного користувача.

    **Аргументи:**
    - **body**: Дані для створення продукту (назва, гаманець, ціна).
    - **product_service**: Сервіс для роботи з продуктами (ін'єкція через Dishka).
    - **current_user**: Поточний авторизований користувач (отриманий через залежність).

    **Повертає:**
    - Об'єкт створеного продукту у форматі ProductResponseSch.

    **Помилки:**
    - 400 Bad Request: Якщо ціна або адреса гаманця невалідні.
    - 500 Internal Server Error: Непередбачена помилка сервера.
    """
    try:
        # Викликаємо бізнес-логіку створення продукту через сервіс
        product = await product_service.create_product(
            title=body.title,
            wallet_address=body.wallet_address,
            price=body.price,
            user_id=current_user.id
        )
        # Валідуємо та повертаємо результат через Pydantic схему
        return ProductResponseSch.model_validate(product)

    except (InvalidPriceError, InvalidWalletAddressError, ValueError) as e:
        # Обробка очікуваних помилок валідації бізнес-логіки
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except Exception as e:
        # Логування непередбачених помилок для подальшого аналізу
        logger.error(f"Unexpected error creating product: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера при создании продукта."
        )
