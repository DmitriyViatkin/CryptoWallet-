from dishka import Provider, provide, Scope
from pwdlib import PasswordHash

from src.auth.services.jwt_serv import JWTService
from src.auth.services.auth_serv import AuthService
from src.users.repositories.user_repo import UserRepository
from src.users.repositories.permission_repo import PermissionRepository


class AuthProvider(Provider):
    scope = Scope.REQUEST

    jwt_service = provide(JWTService)

    @provide(scope=Scope.REQUEST)
    def auth_service(
        self,
        user_repo: UserRepository,
        permission_repo: PermissionRepository,
        jwt_service: JWTService,
    ) -> AuthService:

        password_hash = PasswordHash.recommended()

        return AuthService(
            user_repo=user_repo,
            permission_repo=permission_repo,
            jwt_service=jwt_service,
            password_hash=password_hash,
        )