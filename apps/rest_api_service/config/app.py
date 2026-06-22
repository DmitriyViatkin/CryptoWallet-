import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_pagination import add_pagination
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.ioc import container  # ← забыли
from config.settings import auth_settings
from config.infra.builder import FastAPIBuilder
from src.tasks.broker import broker
from src.auth.routers.router import router as auth_router
from src.users.routers.product_rout.product_rout import router as product_router
from src.users.routers.users.user_router import router as user_router
from src.users.routers.wallets.wallet_router import router as wallet_router
from src.users.services.bootstrap_service import sync_wallets_to_redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()

    async with container() as c:
        redis = await c.get(Redis)
        session_factory = await c.get(async_sessionmaker[AsyncSession])

    asyncio.create_task(
        sync_wallets_to_redis(session_factory, redis)
    )
    yield
    await broker.shutdown()


builder = FastAPIBuilder(
    title=auth_settings.TITLE,
    description=auth_settings.DESCRIPTION,
    lifespan=lifespan
)
app = builder.get_app()
add_pagination(app)
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(wallet_router)