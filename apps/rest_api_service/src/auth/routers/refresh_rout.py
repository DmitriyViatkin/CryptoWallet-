from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject

from src.auth.services.auth_serv import AuthService
from src.auth.dependencies import get_current_user
from src.auth.schemas.login_sch import LoginRequest
from src.auth.schemas.register_sch import RegisterRequest
from src.auth.schemas.refresh_sch import RefreshRequest
from src.auth.schemas.token_sch import TokenResponse
from src.auth.schemas.user_resp_sch import UserResponse
from src.users.models.users import User

router = APIRouter( )


@router.post("/refresh", response_model=TokenResponse)
@inject
async def refresh(
    body: RefreshRequest,
    auth_service: FromDishka[AuthService],
) -> dict:
    try:
        return await auth_service.refresh_token(body.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


