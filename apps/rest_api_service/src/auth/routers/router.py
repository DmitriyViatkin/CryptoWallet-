from fastapi import APIRouter\

from .login_rout import router as login_router
from .register_rout import router as register_router
from .refresh_rout import router as refresh_router
from .me_rout import router as me_router
from .reset_password_rout import router as reset_password_router
from .forgot_password_rout import router as forgot_password_router


router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(register_router)
router.include_router(login_router)
router.include_router(forgot_password_router)
router.include_router(reset_password_router)
#router.include_router(refresh_router)
router.include_router(me_router)