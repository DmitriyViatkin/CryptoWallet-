"""Dependency injection container configuration.

This module sets up the dishka IoC (Inversion of Control) container
with all application providers for dependency injection.
"""

from dishka import make_async_container
from faststream.rabbit import RabbitBroker


from config.infra.config.base_settings import InfraSettings
from config.infra.config.base_settings import infra_settings
from config.infra.providers.redis_provider import RedisProvider
from config.infra.providers.postgres_provider import PostgresProvider
from config.infra.providers.rabbit_provider import RabbitProvider
from config.infra.providers.rest_app_providers import RestAppProviders
from config.infra.providers.jwt_provider import JWTProviders
from config.infra.providers.auth_provider import AuthProvider



# Create async DI container with all providers and settings
container = make_async_container(
    # Data store providers
    RedisProvider(),
    PostgresProvider(),
    RabbitProvider(),
    RestAppProviders(),
    JWTProviders(),
AuthProvider(),

    # Global context settings
    context={InfraSettings: infra_settings}
)

