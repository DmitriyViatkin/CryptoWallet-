from dishka import Provider, Scope, provide
from src.services.web3_wallet_service import Web3WalletService


class WalletProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_wallet_service(self) -> Web3WalletService:
        return Web3WalletService()