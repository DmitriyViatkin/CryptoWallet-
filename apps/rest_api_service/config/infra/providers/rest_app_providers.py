from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.users.repositories import (
    UserRepository, PermissionRepository, WalletRepository,
    WalletOperationRepository, OrderRepository, ProductRepository
)
from src.users.services import (
    UserService, WalletService, OrderService, ProductService
)



class RestAppProviders(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_user_repo(self, session: AsyncSession) -> UserRepository:
        return UserRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_permission_repo(self, session: AsyncSession) -> PermissionRepository:
        return PermissionRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_wallet_repo(self, session: AsyncSession) -> WalletRepository:
        return WalletRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_wallet_operation_repo(self, session: AsyncSession) -> WalletOperationRepository:
        return WalletOperationRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_order_repo(self, session: AsyncSession) -> OrderRepository:
        return OrderRepository(session)

    @provide(scope=Scope.REQUEST)
    def provide_product_repo(self, session: AsyncSession) -> ProductRepository:
        return ProductRepository(session)

    # ── Services ──────────────────────────────────────────────────────────────

    @provide(scope=Scope.REQUEST)
    def provide_user_service(
            self,
            user_repo: UserRepository,
            permission_repo: PermissionRepository,
    ) -> UserService:
        return UserService(user_repo, permission_repo)

    @provide(scope=Scope.REQUEST)
    def provide_wallet_service(
            self,
            wallet_repo: WalletRepository,
            wallet_operation_repo: WalletOperationRepository,
    ) -> WalletService:
        return WalletService(wallet_repo, wallet_operation_repo)

    @provide(scope=Scope.REQUEST)
    def provide_order_service(
            self,
            order_repo: OrderRepository,
            product_repo: ProductRepository,
    ) -> OrderService:
        return OrderService(order_repo, product_repo)

    @provide(scope=Scope.REQUEST)
    def provide_product_service(
            self,
            product_repo: ProductRepository,
    ) -> ProductService:
        return ProductService(product_repo)

