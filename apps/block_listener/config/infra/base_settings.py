"""Infrastructure configuration settings for block_listener service."""

from pathlib import Path
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


# --- BASE ---
class BaseInfraSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )


# --- REDIS (1-в-1 как в auth_service, для консистентности) ---
class RedisSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
    )

    HOST: str = "localhost"
    PORT: int = 6379
    PASSWORD: Optional[str] = None
    DB: int = 1  # ВАЖНО: другая DB-нумерация, чтобы не конфликтовать с auth_service (у него скорее всего DB=0)

    @property
    def url(self) -> str:
        if self.PASSWORD:
            return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


# --- RABBITMQ (1-в-1 как в auth_service — общая шина) ---
class RabbitMQSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="RABBITMQ_",
    )

    HOST: str = "localhost"
    PORT: int = 5672
    USER: str = "guest"
    PASSWORD: str = "guest"
    VHOST: str = "/"

    @property
    def url(self) -> str:
        vhost = self.VHOST.lstrip("/")
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{vhost}"


# --- ALCHEMY (новое — специфично для block_listener) ---
class AlchemySettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="ALCHEMY_",
    )

    WS_URL: str  # обязательное поле, без default — сервис не должен стартовать без него
    RECONNECT_DELAY_SEC: int = 5
    MAX_RECONNECT_DELAY_SEC: int = 60
    RESYNC_INTERVAL_SEC: int = 3600  # для периодической реконсиляции адресов, обсуждали выше




# --- MAIN ---
class InfraSettings(BaseInfraSettings):
    redis: RedisSettings = Field(default_factory=RedisSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    alchemy: AlchemySettings = Field(default_factory=AlchemySettings)


@lru_cache
def get_infra_settings() -> InfraSettings:
    return InfraSettings()


infra_settings: InfraSettings = get_infra_settings()
redis_settings = infra_settings.redis
rabbitmq_settings = infra_settings.rabbitmq
alchemy_settings = infra_settings.alchemy