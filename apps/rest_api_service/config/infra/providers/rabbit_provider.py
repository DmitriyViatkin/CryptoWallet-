"""RabbitMQ message broker provider for dependency injection.

This module defines the Dishka provider for RabbitMQ broker connections
using async FastStream broker.
"""

from typing import AsyncGenerator

from faststream.rabbit import RabbitBroker
from dishka import Provider, Scope, provide

from apps.rest_api_service.config.infra.config.base_settings import InfraSettings


class RabbitProvider(Provider):
    """Provides RabbitMQ broker connection via dependency injection.

    Creates and manages RabbitMQ broker connections using FastStream
    framework. Ensures proper lifecycle management with startup and shutdown.
    """

    @provide(scope=Scope.APP)
    async def provide_rabbit(self, infra_settings: InfraSettings) -> AsyncGenerator[RabbitBroker, None]:
        """Create and manage RabbitMQ broker connection.

        Creates a RabbitMQ broker connection at APP scope with automatic
        lifecycle management. The broker is started when the application
        starts and stopped when it shuts down.

        Args:
            infra_settings: Infrastructure configuration containing RabbitMQ settings.

        Yields:
            RabbitBroker: Connected RabbitMQ broker instance ready for publishing
                         and consuming messages.
        """
        broker = RabbitBroker(infra_settings.rabbitmq.url)
        yield broker
        # Gracefully stop broker when application shuts down
        await broker.stop()

