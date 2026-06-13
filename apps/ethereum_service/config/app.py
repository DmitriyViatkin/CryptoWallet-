from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from config.settings import auth_settings
from config.infra.builder import FastAPIBuilder

# ← всі імпорти через src., не через ethereum_service.src.



@asynccontextmanager
async def lifespan(app: FastAPI):
    from config.ioc import container
    from faststream.rabbit import RabbitBroker
    broker = await container.get(RabbitBroker)  # запускает провайдер
    yield


builder = FastAPIBuilder(
    title=auth_settings.TITLE,
    description=auth_settings.DESCRIPTION,
    lifespan=lifespan,
)
app = builder.get_app()
add_pagination(app)

