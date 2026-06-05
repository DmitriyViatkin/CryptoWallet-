from datetime import datetime, timedelta, timezone

import jwt

from config.settings import auth_settings


class JWTService:
    def __init__(self) -> None:
        self._secret = auth_settings.SECRET_KEY
        self._algorithm = auth_settings.ALGORITHM
        self._access_expire = auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_expire = auth_settings.REFRESH_TOKEN_EXPIRE_DAYS
        self._reset_expire = getattr(auth_settings, "RESET_TOKEN_EXPIRE_MINUTES", 15)

    def create_access_token(self, user_id: int) -> str:
        return self._encode(
            {"sub": str(user_id), "type": "access"},
            timedelta(minutes=self._access_expire),
        )

    def create_refresh_token(self, user_id: int) -> str:
        return self._encode(
            {"sub": str(user_id), "type": "refresh"},
            timedelta(days=self._refresh_expire),
        )

    def create_reset_token(self, user_id: int) -> str:
        return self._encode(
            {"sub": str(user_id), "type": "reset"},
            timedelta(minutes=self._reset_expire),
        )

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algorithm])

    def _encode(self, payload: dict, expires_delta: timedelta) -> str:
        payload["exp"] = datetime.now(timezone.utc) + expires_delta
        return jwt.encode(payload, self._secret, algorithm=self._algorithm)