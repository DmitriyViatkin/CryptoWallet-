from fastapi import HTTPException, Request, status
from redis.asyncio import Redis
from dishka.integrations.fastapi import FromDishka, inject

RATE_LIMIT_PREFIX = "rl:"
MAX_REQUESTS = 100
WINDOW_SECONDS = 15  # 15 секунд


def make_rate_limiter(max_requests: int = MAX_REQUESTS, window_seconds: int = WINDOW_SECONDS):
    @inject
    async def _limiter(request: Request, redis: FromDishka[Redis]) -> None:
        ip = request.client.host
        key = f"{RATE_LIMIT_PREFIX}{ip}:{request.url.path}"

        count = await redis.incr(key)
        if count == 1:
            await redis.expire(key, window_seconds)

        if count > max_requests:
            ttl = await redis.ttl(key)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Too many requests. Retry after {ttl}s.",
                headers={"Retry-After": str(ttl)},
            )

    return _limiter


rate_limiter = make_rate_limiter()