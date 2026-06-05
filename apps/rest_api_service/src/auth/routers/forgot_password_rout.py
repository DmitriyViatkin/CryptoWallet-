# src/auth/routers/forgot_password_rout.py
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.schemas.forgot_password_sch import ForgotPasswordRequest
from src.auth.services.auth_serv import AuthService
from src.auth.rate_limit import rate_limiter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[Depends(rate_limiter)],
)
@inject
async def forgot_password(
    body: ForgotPasswordRequest,
    auth_service: FromDishka[AuthService],
) -> dict:
    # AuthService сам: Redis.save() + EventPublisher → RabbitMQ → FastStream → SMTP
    await auth_service.request_password_reset(body.email)
    return {"detail": "If this email exists, a reset link has been sent"}