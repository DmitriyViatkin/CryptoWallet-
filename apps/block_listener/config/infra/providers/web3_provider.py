from dishka import Provider, Scope, provide

from config.infra.base_settings import infra_settings
from src.core.ws_client import AlchemyWSClient


class Web3Provider(Provider):
    @provide(scope=Scope.APP)
    def get_ws_client(self) -> AlchemyWSClient:
        alchemy = infra_settings.alchemy
        return AlchemyWSClient(
            ws_url=alchemy.WS_URL,
            reconnect_delay=alchemy.RECONNECT_DELAY_SEC,
            max_delay=alchemy.MAX_RECONNECT_DELAY_SEC,
        )