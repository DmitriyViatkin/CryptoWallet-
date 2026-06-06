from fastapi import APIRouter
from .me_rout import router as me_router
from .user_update_rout import router as user_update_router

router = APIRouter(prefix="/users", tags=["users"])


router.include_router(me_router)
router.include_router(user_update_router)

