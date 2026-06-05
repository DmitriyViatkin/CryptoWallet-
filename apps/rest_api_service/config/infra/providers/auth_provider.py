# config/infra/providers/auth_provider.py
from dishka import Provider, provide, Scope
from faststream.rabbit import RabbitBroker
from pwdlib import PasswordHash
from redis.asyncio import Redis

from src.auth.services.auth_serv import AuthService
from src.auth.services.jwt_serv import JWTService
from src.auth.services.reset_token_serv import ResetTokenService
from src.publisher import EventPublisher
from src.users.repositories.permission_repo import PermissionRepository
from src.users.repositories.user_repo import UserRepository


class AuthProvider(Provider):
    scope = Scope.REQUEST

    jwt_service = provide(JWTService)

    @provide(scope=Scope.APP)
    def event_publisher(self, broker: RabbitBroker) -> EventPublisher:
        return EventPublisher(broker)

    @provide(scope=Scope.APP)
    def get_reset_token_service(self, redis: Redis) -> ResetTokenService:
        return ResetTokenService(redis)

    @provide
    def auth_service(
        self,
        user_repository: UserRepository,
        permission_repository: PermissionRepository,
        jwt_service: JWTService,
        reset_token_service: ResetTokenService,
        event_publisher: EventPublisher,
    ) -> AuthService:
        return AuthService(
            user_repo=user_repository,
            permission_repo=permission_repository,
            jwt_service=jwt_service,
            password_hash=PasswordHash.recommended(),
            reset_token_service=reset_token_service,
            event_publisher=event_publisher,
        )