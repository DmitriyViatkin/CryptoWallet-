from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject
from..schemas.forgot_password_sch import ForgotPasswordRequest
from..schemas.reset_password_request_sch import ResetPasswordRequest
from src.auth.services.auth_serv import AuthService
from src.auth.rate_limit import rate_limiter
#from src.tasks.email_tasks import send_reset_email  # твій TaskIQ таск

router = APIRouter()


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(rate_limiter)],
)
@inject
async def reset_password(
    body: ResetPasswordRequest,
    auth_service: FromDishka[AuthService],
) -> dict:
    try:
        await auth_service.confirm_password_reset(body.token, body.new_password)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"detail": "Password successfully reset"}