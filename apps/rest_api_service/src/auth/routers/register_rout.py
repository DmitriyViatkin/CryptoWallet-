from fastapi import APIRouter, HTTPException, status
from dishka.integrations.fastapi import FromDishka, inject
import traceback

from src.auth.services.auth_serv import AuthService
from src.auth.schemas.register_sch import RegisterRequest
from src.auth.schemas.user_resp_sch import UserResponse
from src.users.models.users import User

from src.auth.exceptions import (
    UserAlreadyExistsError,
    EmailAlreadyExistsError,
    WeakPasswordError,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
@inject
async def register(
    body: RegisterRequest,
    auth_service: FromDishka[AuthService],
) -> User:

    try:
        return await auth_service.register(
            username=body.username,
            email=body.email,
            password=body.password,
        )

    except UserAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "USERNAME_TAKEN",
                "message": "Пользователь с таким username уже существует."
            }
        )

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": "EMAIL_TAKEN",
                "message": "Пользователь с таким email уже существует."
            }
        )

    except WeakPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "WEAK_PASSWORD",
                "message": str(e)
            }
        )

    except Exception as e:
        traceback.print_exc()
        raise