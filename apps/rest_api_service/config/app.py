import mimetypes
from fastapi.staticfiles import StaticFiles

# Импортируем готовый инстанс настроек вместо класса
from config.settings import auth_settings
from config.infra.builder import FastAPIBuilder
from src.auth.routers.router import router as auth_router
from src.users.routers.product_rout.product_rout import router as product_router
# Инициализируем билдер, передавая значения из инстанса auth_settings
builder = FastAPIBuilder(
    title=auth_settings.TITLE,
    description=auth_settings.DESCRIPTION,
)
app = builder.get_app()



# Подключаем роуты аутентификации
app.include_router(auth_router)
app.include_router(product_router)