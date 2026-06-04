from fastapi import APIRouter

from .product_delete_rout import router as product_delete_router
from .product_create_rout import router as product_create_router
from .product_update_rout import router as product_update_router
from .product_all_rout import router as product_all_router
from .product_users_rout import router as product_users_router
router = APIRouter(prefix="/product", tags=["product"])

router.include_router(product_all_router)

router.include_router(product_users_router)
router.include_router(product_create_router)
router.include_router(product_update_router)

router.include_router(product_delete_router)