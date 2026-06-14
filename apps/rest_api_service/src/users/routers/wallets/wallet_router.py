from .import_router import router as import_router
from .get_job_status import router as get_job_status_router
from .create_wallet import router as create_wallet_router
from fastapi import  APIRouter

router = APIRouter(prefix="/wallets", tags=["wallets"])

router.include_router(import_router)
#router.include_router(get_job_status_router)
router.include_router(create_wallet_router)

