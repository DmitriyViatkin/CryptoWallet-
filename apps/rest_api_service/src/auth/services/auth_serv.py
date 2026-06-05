import jwt
from pwdlib import PasswordHash
from src.publisher import EventPublisher
from src.auth.services.jwt_serv import JWTService
from src.auth.services.reset_token_serv import ResetTokenService
from src.users.models.users import User
from src.users.repositories.user_repo import UserRepository
from src.users.repositories.permission_repo import PermissionRepository

from src.tasks.access_chat import enable_chat_access_task
from src.auth.exceptions import EmailAlreadyExistsError


class AuthService:
    def __init__(
        self,
        user_repo: UserRepository,
        permission_repo: PermissionRepository,
        jwt_service: JWTService,
        password_hash: PasswordHash,
        reset_token_service: ResetTokenService,
        event_publisher: EventPublisher,        # ← додати
    ) -> None:
        self._user_repo = user_repo
        self._permission_repo = permission_repo
        self._jwt = jwt_service
        self._password_hash = password_hash
        self._reset_tokens = reset_token_service
        self._event_publisher = event_publisher
    def hash_password(self, password: str) -> str:
        return self._password_hash.hash(password)

    def verify_password(self, plain: str, hashed: str) -> bool:
        return self._password_hash.verify(plain, hashed)

    async def register(self, username: str, email: str, password: str) -> User:
        existing = await self._user_repo.get_by_email(email)

        if existing:
            raise EmailAlreadyExistsError()

        user = await self._user_repo.create(
            username=username,
            email=email,
            hashed_password=self.hash_password(password),
        )

        await self._permission_repo.create(
            user_id=user.id,
            has_chat_access=False,
        )

        await self._event_publisher.publish_user_registered(
            user_id=user.id,
            email=user.email,
        )

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

    async def request_password_reset(self, email: str) -> None:
        user = await self._user_repo.get_by_email(email)
        if user is None:
            return
        token = self._jwt.create_reset_token(user.id)          # _jwt, не _jwt_service
        await self._reset_tokens.save(token, user.id)          # _reset_tokens, не _reset_token_service
        await self._event_publisher.publish_password_reset(
            to_email=user.email,
            reset_token=token,
            user_id=user.id,
        )

    async def confirm_password_reset(
        self,
        token: str,
        new_password: str,
    ) -> None:
        user_id = await self._reset_tokens.get_user_id(token)  # _reset_tokens
        if user_id is None:
            raise ValueError("Invalid or expired reset token")
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")
        hashed = self._password_hash.hash(new_password)        # _password_hash
        await self._user_repo.update(user, hashed_password=hashed)
        await self._reset_tokens.invalidate(token)