from typing import AsyncGenerator

from dishka import Provider, Scope, provide
from faststream.rabbit import RabbitBroker

from config.infra.base_settings import InfraSettings
from config.infra.faststream_app import rabbit_router


class RabbitProvider(Provider):

    @provide(scope=Scope.APP)
    async def provide_rabbit(
        self,
        infra_settings: InfraSettings,
    ) -> AsyncGenerator[RabbitBroker, None]:
        broker = RabbitBroker(
            url=infra_settings.rabbitmq.url,
            graceful_timeout=30,  # чекає завершення handlers при shutdown
        )

        # Підключаємо router зі subscribers ДО старту
        broker.include_router(rabbit_router)

        # Стартуємо — підключення до RabbitMQ, оголошення exchanges/queues,
        # початок прослуховування черг
        await broker.start()

        yield broker

        # Dishka викличе це при shutdown FastAPI app
        await broker.close()