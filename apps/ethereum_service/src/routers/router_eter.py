from ethereum_service.src.routers.router_jobs import router as jobs_router
from ethereum_service.src.routers.router_import_wallet import router as import_wallet_router

from fastapi import APIRouter

router = APIRouter(prefix="/wallets", tags=["wallets"], )

router.include_router(jobs_router)
router.include_router(import_wallet_router)