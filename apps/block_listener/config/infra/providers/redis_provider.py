from redis.asyncio import Redis
from dishka import Provider, Scope, provide

from config.infra.base_settings import redis_settings


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_redis(self) -> Redis:
        return Redis.from_url(
            redis_settings.url,
            encoding="utf-8",
            decode_responses=True,
        )