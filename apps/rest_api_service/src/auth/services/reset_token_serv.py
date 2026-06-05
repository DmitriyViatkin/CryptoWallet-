from redis.asyncio import Redis

RESET_TOKEN_PREFIX = "reset:"
RESET_TOKEN_TTL = 60 * 30  # 30 хвилин — збігається з JWT exp


class ResetTokenService:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def _key(self, token: str) -> str:
        return f"{RESET_TOKEN_PREFIX}{token}"

    async def save(self, token: str, user_id: int) -> None:
        await self._redis.setex(self._key(token), RESET_TOKEN_TTL, str(user_id))

    async def get_user_id(self, token: str) -> int | None:
        value = await self._redis.get(self._key(token))
        return int(value) if value else None

    async def invalidate(self, token: str) -> None:
        """Одноразовий токен — видаляємо одразу після використання."""
        await self._redis.delete(self._key(token))