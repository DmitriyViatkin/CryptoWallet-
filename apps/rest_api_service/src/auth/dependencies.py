import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dishka.integrations.fastapi import FromDishka, inject
from src.auth.services.auth_serv import AuthService
from src.auth.services.jwt_serv import JWTService
from src.users.models.users import User

oauth2_scheme = HTTPBearer()

@inject
async def get_current_user(
    auth_service: FromDishka[AuthService],
    jwt_service: FromDishka[JWTService],
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),  # ← виправлено
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials  # ← витягуємо сам токен

    try:
        payload = jwt_service.decode(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise credentials_exception

    if payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("sub")
    if not user_id:
        raise credentials_exception

    user = await auth_service.get_user_by_id(int(user_id))
    if not user or not user.is_active:
        raise credentials_exception

    return user