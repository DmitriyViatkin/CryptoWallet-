from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from config.infra.providers.rabbit_broker import broker


class RabbitProvider(Provider):
    @provide(scope=Scope.APP)
    def get_broker(self) -> RabbitBroker:
        # Тот же broker, что слушает FastStream-приложение —
        # запуск/остановку им управляет сам FastStream runtime,
        # здесь просто отдаём ссылку для инъекции в сервисы
        return broker