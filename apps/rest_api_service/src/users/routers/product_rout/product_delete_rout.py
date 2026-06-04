import logging
from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject
from src.users.services.product_serv import ProductService
from src.users.schemas.product_sch.product_update_sch import ProductUpdateSch
from src.users.schemas.product_sch.product_resp_sch import ProductResponseSch
from src.auth.dependencies import get_current_user
from src.exception.product_except import (
    InvalidPriceError,
    InvalidWalletAddressError,
    ProductNotFoundError,
    ProductAccessDeniedError
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.delete("/{pk}/delete", status_code=status.HTTP_204_NO_CONTENT,
               summary="Видалення продукту користувача")
@inject
async def delete_product(
    pk: int,
    product_service: FromDishka[ProductService],
    current_user=Depends(get_current_user))-> None:
    """
    Видалення продукту користувача.
    - Перевірка що product.user_id == user_id
    - Перевірка що продукт не використовується в активних замовленнях
    """
    try:
        await product_service.delete_product(
            product_id=pk, user_id=current_user.id)
    except ProductNotFoundError:
        logger.warning(f"Продукт с id {pk} не найден для удаления.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Продукт не найден.")
    except ProductAccessDeniedError:
        logger.warning(
            f"Пользователь {current_user.id} попытался удалить продукт {pk},"
            f" который ему не принадлежит.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="У вас нет прав на удаление этого продукта.")
    #except Exception as e:
        #logger.error(f"Ошибка при удалении продукта {pk}: {str(e)}")
        #raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                  #          detail="Ошибка сервера при удалении продукта.")


