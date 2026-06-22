from .import_router import router as import_router
from .get_job_status import router as get_job_status_router
from .create_wallet import router as create_wallet_router
from .get_transaction_wallet import router as get_transaction_wallet_router
from .get_transaction import router as get_transaction_router
from .all_wallet_user import router as all_wallet_user_router
from .send_transaction import router as send_transaction_router
from fastapi import  APIRouter


router = APIRouter(prefix="/wallets", tags=["wallets"])
router.include_router(all_wallet_user_router)
router.include_router(import_router)
#router.include_router(get_job_status_router)
router.include_router(create_wallet_router)
router.include_router(get_transaction_wallet_router)
router.include_router(get_transaction_router)
router.include_router(send_transaction_router)
