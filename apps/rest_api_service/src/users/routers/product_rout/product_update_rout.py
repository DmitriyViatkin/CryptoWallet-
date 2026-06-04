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


@router.put("/update", response_model=ProductResponseSch,
            status_code= status.HTTP_200_OK)
@inject

async def update_product(
                        body: ProductUpdateSch,
                        product_service: FromDishka[ProductService],
                        current_user=Depends(get_current_user)):

    try:

        update_data = body.model_dump(exclude_unset=True) # превращаю схему в словарь только с заповненими полями всі нон пропустим

        product_id = update_data.pop("product_id")# получаю id продукта


        product = await product_service.update_product(
            product_id = product_id,
            user_id = current_user.id,
            **update_data
            )
        return ProductResponseSch.model_validate(product)
    except (InvalidPriceError, InvalidWalletAddressError, ValueError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ProductNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ProductAccessDeniedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    #except Exception:
        #raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           # detail="Внутренняя ошибка сервера при обновлении продукта.")

