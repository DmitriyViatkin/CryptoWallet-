from .product_delete_rout import router as product_delete_router
from .product_create_rout import router as product_create_router
from .product_rout import router as product_router
from .product_update_rout import router as product_update_router

__all__=[
    "product_delete_router",
    "product_create_router",
    "product_router",
    "product_update_router"
]