from faststream import FastStream
from faststream.rabbit import RabbitBroker



class FastStreamBuilder:
    """FastStream app builder, зеркало FastAPIBuilder из других сервисов."""

    def __init__(self, broker: RabbitBroker, title: str, description: str):
        self.broker = broker
        self.app: FastStream = self.build_app(broker, title, description)
        self.register_di_container()

    @staticmethod
    def build_app(broker: RabbitBroker, title: str, description: str) -> FastStream:
        """Build FastStream app."""
        return FastStream(
            broker

        )

    def get_app(self) -> FastStream:
        """Return FastStream app instance"""
        return self.app

    def register_di_container(self) -> None:
        """Inject dependencies into FastStream"""
        from config.ioc import container
        from dishka.integrations.faststream import setup_dishka

        setup_dishka(container=container, app=self.app)