import mimetypes
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
# Импортируем готовый инстанс настроек вместо класса
from config.settings import auth_settings
from config.infra.builder import FastAPIBuilder

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.tasks.broker import broker

from src.auth.routers.router import router as auth_router
from src.users.routers.product_rout.product_rout import router as product_router
from src.users.routers.users.user_router import router as user_router
from src.users.routers.wallets.wallet_router import router as wallet_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.startup()
    yield
    await broker.shutdown()


builder = FastAPIBuilder(
    title=auth_settings.TITLE,
    description=auth_settings.DESCRIPTION,
    lifespan=lifespan
)
app = builder.get_app()
add_pagination(app)


# Подключаем роуты аутентификации
app.include_router(auth_router)
app.include_router(product_router)
app.include_router(user_router)

app.include_router(wallet_router)