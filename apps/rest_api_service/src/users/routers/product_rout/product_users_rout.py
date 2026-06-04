import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from dishka.integrations.fastapi import FromDishka, inject
from src.users.services.product_serv import ProductService
from src.users.schemas.product_sch.product_update_sch import ProductUpdateSch
from src.users.schemas.product_sch.product_resp_sch import ProductResponseSch
from src.users.schemas.product_sch.product_list_response_sch import ProductListResponseSch
from fastapi_pagination import Page, paginate

from src.auth.dependencies import get_current_user
from src.exception.product_except import (
    InvalidPriceError,
    InvalidWalletAddressError,
    ProductNotFoundError,
    ProductAccessDeniedError
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/user_product", status_code= status.HTTP_200_OK,
            response_model= Page[ProductResponseSch],
            summary="Получение всех продуктов текущего пользователя")
@inject
async def get_user_product(
        product_service: FromDishka[ProductService],
        current_user=Depends(get_current_user)
):
    try:
        products = await product_service.get_user_products(user_id=current_user.id)
        return paginate(products if products is not None else [])
    except Exception as e:
        logger.error(f"Помилка при отриманні продуктів користувача: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутрішня помилка сервера при отриманні продуктів."
        )