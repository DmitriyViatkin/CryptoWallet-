"""Dependency injection container configuration.

This module sets up the dishka IoC (Inversion of Control) container
with all application providers for dependency injection.
"""

"""Dependency injection container configuration for block_listener."""

from dishka import make_async_container

from config.infra.base_settings import InfraSettings, infra_settings
from config.infra.providers.redis_provider import RedisProvider
from config.infra.providers.rabbit_provider import RabbitProvider
from config.infra.providers.web3_provider import Web3Provider
from config.infra.providers.listener_provider import ListenerProvider

container = make_async_container(
    RedisProvider(),
    RabbitProvider(),
    Web3Provider(),
    ListenerProvider(),
    context={InfraSettings: infra_settings},
)







