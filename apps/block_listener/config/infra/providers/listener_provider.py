from dishka import Provider, Scope, provide
from redis.asyncio import Redis
from faststream.rabbit import RabbitBroker

from config.infra.messaging.publisher import TxDetectedPublisher
from src.core.ws_client import AlchemyWSClient
from src.services.listener_service import BlockListenerService


class ListenerProvider(Provider):
    @provide(scope=Scope.APP)
    def get_publisher(self, broker: RabbitBroker) -> TxDetectedPublisher:
        return TxDetectedPublisher(broker=broker)

    @provide(scope=Scope.APP)
    def get_listener_service(
        self,
        ws_client: AlchemyWSClient,
        redis: Redis,
        publisher: TxDetectedPublisher,
    ) -> BlockListenerService:
        return BlockListenerService(ws_client=ws_client, redis=redis, publisher=publisher)