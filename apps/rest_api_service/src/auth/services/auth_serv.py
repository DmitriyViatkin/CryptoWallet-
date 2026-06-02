import jwt
from pwdlib import PasswordHash

from src.auth.services.jwt_serv import JWTService
from src.users.models.users import User
from src.users.repositories.user_repo import UserRepository
from src.users.repositories.permission_repo import PermissionRepository


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        permission_repo: PermissionRepository,
        jwt_service: JWTService,
        password_hash: PasswordHash,  # Внедряем хэшер через Dishka
    ) -> None:
        self._user_repo = user_repo
        self._permission_repo = permission_repo
        self._jwt = jwt_service
        self._password_hash = password_hash  # Сохраняем в инстанс сервиса

    def hash_password(self, password: str) -> str:
        """Хэширование пароля при помощи pwdlib."""
        return self._password_hash.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        """Проверка совпадения пароля при помощи pwdlib."""
        return self._password_hash.verify(plain, hashed)

    async def register(self, username: str, email: str, password: str) -> User:
        existing = await self._user_repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = await self._user_repo.create(
            username=username,
            email=email,
            hashed_password=self.hash_password(password),
        )
        await self._permission_repo.create(user_id=user.id, has_chat_access=False)
        return user

    async def login(self, email: str, password: str) -> dict:
        user = await self._user_repo.get_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        if not user.is_active:
            raise ValueError("User is deactivated")

        return {
            "access_token": self._jwt.create_access_token(user.id),
            "refresh_token": self._jwt.create_refresh_token(user.id),
            "token_type": "bearer",
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = self._jwt.decode(refresh_token)
        except jwt.ExpiredSignatureError:
            raise ValueError("Refresh token expired")
        except jwt.PyJWTError:
            raise ValueError("Invalid refresh token")

        if payload.get("type") != "refresh":
            raise ValueError("Invalid token type")

        user_id = int(payload["sub"])
        return {
            "access_token": self._jwt.create_access_token(user_id),
            "refresh_token": self._jwt.create_refresh_token(user_id),
            "token_type": "bearer",
        }

    async def get_user_by_id(self, user_id: int) -> User | None:
        return await self._user_repo.get_by_id(user_id)