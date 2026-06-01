"""Dependency injection container configuration.

This module sets up the dishka IoC (Inversion of Control) container
with all application providers for dependency injection.
"""

from dishka import make_async_container

from apps.rest_api_service.config.infra.config.base_settings import InfraSettings
from infra.config.base_settings import infra_settings
from infra.providers.redis_provider import RedisProvider
from infra.providers.postgres_provider import PostgresProvider
from infra.providers.rabbit_provider import RabbitProvider

# Create async DI container with all providers and settings
container = make_async_container(
    # Data store providers
    RedisProvider(),
    PostgresProvider(),
    RabbitProvider(),

    # Global context settings
    context={InfraSettings: infra_settings}
)

