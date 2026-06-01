"""Redis cache provider for dependency injection.

This module defines the Dishka provider for Redis cache connections
using async Redis client.
"""

from redis.asyncio import Redis
from dishka import Provider, Scope, provide


class RedisProvider(Provider):
    """Provides Redis cache client via dependency injection.

    Creates and manages async Redis connections at APP scope using Dishka
    framework for dependency injection.
    """

    @provide(scope=Scope.APP)
    async def get_redis(self) -> Redis:
        """Create async Redis connection.

        Creates a Redis client at APP scope - instantiated once per application
        lifetime and reused across all requests.

        Returns:
            Redis: Connected async Redis client instance.
        """
        return Redis(host="localhost", port=6379, db=0)

