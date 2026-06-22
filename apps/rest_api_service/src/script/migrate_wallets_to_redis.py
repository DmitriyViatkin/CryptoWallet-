# scripts/migrate_wallets_to_redis.py (в auth_service)
import asyncio
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

DATABASE_URL = "postgresql+asyncpg://Owner:Owner12345@localhost:5432/rest_api_db"
REDIS_URL = "redis://localhost:6379/0"

async def main():
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine)
    r = redis.from_url(REDIS_URL, decode_responses=True)

    async with async_session() as session:
        result = await session.execute(text("SELECT wallet_address FROM wallets"))
        addresses = [row[0].lower() for row in result.fetchall()]

    if addresses:
        await r.sadd("wallets:addresses", *addresses)
        print(f"Migrated {len(addresses)} addresses to Redis")
    else:
        print("No wallets found")

    await r.aclose()
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())