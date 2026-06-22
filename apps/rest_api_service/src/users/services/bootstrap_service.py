import asyncio
import logging
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from redis.asyncio import Redis

logger = logging.getLogger(__name__)


async def sync_wallets_to_redis(
    session_factory: async_sessionmaker[AsyncSession],
    redis: Redis,
) -> None:
    await asyncio.sleep(10)

    async with session_factory() as session:
        result = await session.execute(
            text("SELECT wallet_address FROM wallets")
        )
        addresses = [row[0].lower() for row in result.fetchall()]

    if addresses:
        await redis.sadd("wallets:addresses", *addresses)
        logger.info(f"Bootstrap: synced {len(addresses)} wallets to Redis")
    else:
        logger.warning("Bootstrap: no wallets in DB yet")