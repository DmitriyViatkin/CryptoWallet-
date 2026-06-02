"""Infrastructure configuration settings module.

This module defines configuration classes for all infrastructure services:
- Database (PostgreSQL)
- Redis cache
- RabbitMQ message broker
- SMTP email service
- TaskIQ task queue configuration
"""

from typing import Any, Optional
from pathlib import Path
from functools import lru_cache

from pydantic import PrivateAttr
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- PATHS ---
# Define project root directory and path to .env file
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"


# --- BASE ---
class BaseInfraSettings(BaseSettings):
    """Base infrastructure settings class.

    Provides common configuration for all infrastructure service settings
    with environment variable loading from .env file.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
    )


# --- DATABASE ---
class DatabaseSettings(BaseInfraSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="DB_",
    )

    # Connection parameters
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str
    PASSWORD: str
    DB: str

    # SQLAlchemy
    ECHO: bool = False
    ECHO_POOL: bool = False

    # Pool
    POOL_DISABLED: bool = False
    POOL_SIZE: int = 5
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 3600
    POOL_PRE_PING: bool = True

    # ВАЖНО: не Optional
    POOL_MAX_OVERFLOW: int = 10

    # Private attribute
    _engine_instance: AsyncEngine | None = PrivateAttr(default=None)

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.DB}"
        )

    def _build_engine_params(self) -> dict[str, Any]:
        params: dict[str, Any] = {
            "url": self.url,
            "echo": self.ECHO,
            "echo_pool": self.ECHO_POOL,
            "pool_recycle": self.POOL_RECYCLE,
            "pool_pre_ping": self.POOL_PRE_PING,
        }

        if self.POOL_DISABLED:
            params["poolclass"] = NullPool
            return params

        params.update(
            pool_size=self.POOL_SIZE,
            max_overflow=self.POOL_MAX_OVERFLOW,
            pool_timeout=self.POOL_TIMEOUT,
            pool_use_lifo=True,
        )

        return params

    def get_engine(self) -> AsyncEngine:
        if self._engine_instance is None:
            self._engine_instance = create_async_engine(
                **self._build_engine_params()
            )
        return self._engine_instance

    @property
    def engine(self) -> AsyncEngine:
        return self.get_engine()


# --- REDIS ---
class RedisSettings(BaseInfraSettings):
    """Redis cache configuration settings.

    Manages connection parameters for async Redis connections.
    Loads configuration from environment variables with REDIS_ prefix.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="REDIS_",
    )

    # Connection parameters
    HOST: str = "localhost"  # Redis host
    PORT: int = 6379  # Redis port
    PASSWORD: Optional[str] = None  # Redis password (if authentication required)
    DB: int = 0  # Redis database number

    @property
    def url(self) -> str:
        """Build Redis connection URL.

        Returns:
            str: Redis connection string (redis://...)
        """
        if self.PASSWORD:
            return f"redis://:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}"
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"


# --- TASKIQ (replacement for Celery) ---
class TaskIQSettings(BaseInfraSettings):
    """TaskIQ async task queue configuration settings.

    Configures TaskIQ with RabbitMQ as broker and Redis as result backend.
    Loads configuration from environment variables with TASKIQ_ prefix.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="TASKIQ_",
    )

    # Broker URL - RabbitMQ (using aio-pika)
    BROKER_URL: str = "amqp://guest:guest@localhost:5672/"
    # Results backend - Redis
    RESULT_BACKEND_URL: str = "redis://localhost:6379/1"

    @property
    def broker_url(self) -> str:
        """Get TaskIQ broker URL.

        Returns:
            str: AMQP broker connection string for RabbitMQ.
        """
        return self.BROKER_URL

    @property
    def result_backend_url(self) -> str:
        """Get TaskIQ results backend URL.

        Returns:
            str: Redis connection string for task results storage.
        """
        return self.RESULT_BACKEND_URL


# --- SMTP ---
class SMTPSettings(BaseInfraSettings):
    """SMTP email configuration settings.

    Manages SMTP server connection parameters for sending emails.
    Loads configuration from environment variables with SMTP_ prefix.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="SMTP_",
    )

    # SMTP server connection parameters
    HOST: str = "smtp.example.com"  # SMTP server host
    PORT: int = 587  # SMTP server port (typically 587 for TLS)
    USER: Optional[str] = None  # SMTP username
    PASSWORD: Optional[str] = None  # SMTP password
    USE_TLS: bool = True  # Use TLS encryption
    USE_SSL: bool = False  # Use SSL encryption
    FROM_EMAIL: Optional[str] = None  # Default sender email address


# --- RABBITMQ ---
class RabbitMQSettings(BaseInfraSettings):
    """RabbitMQ message broker configuration settings.

    Manages RabbitMQ connection parameters for async message publishing
    and consuming. Loads configuration from environment variables with
    RABBITMQ_ prefix.
    """
    model_config = SettingsConfigDict(
        env_file=str(ENV_PATH),
        env_file_encoding="utf-8",
        extra="ignore",
        env_prefix="RABBITMQ_",
    )

    # RabbitMQ connection parameters
    HOST: str = "localhost"  # RabbitMQ host
    PORT: int = 5672  # RabbitMQ port
    USER: str = "guest"  # RabbitMQ username
    PASSWORD: str = "guest"  # RabbitMQ password
    VHOST: str = "/"  # RabbitMQ virtual host

    @property
    def url(self) -> str:
        """Build RabbitMQ connection URL.

        Returns:
            str: AMQP connection string (amqp://user:password@host:port/vhost).
        """
        return (
            f"amqp://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.VHOST}"
        )


# --- MAIN ---
class InfraSettings(BaseInfraSettings):
    """Main infrastructure settings container.

    Aggregates configuration for all infrastructure services:
    database, cache, message broker, task queue, and SMTP.
    """
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)  # Database settings
    redis: RedisSettings = Field(default_factory=RedisSettings)  # Redis cache settings
    taskiq: TaskIQSettings = Field(default_factory=TaskIQSettings)  # Task queue settings
    smtp: SMTPSettings = Field(default_factory=SMTPSettings)  # Email settings
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)  # Message broker settings


@lru_cache
def get_infra_settings() -> InfraSettings:
    """Get cached infrastructure settings instance.

    Returns:
        InfraSettings: Singleton instance of all infrastructure settings.
                      Cached to prevent repeated initialization.
    """
    return InfraSettings()


# Global infrastructure settings instance
infra_settings: InfraSettings = get_infra_settings()
db_settings = infra_settings.db  # Database settings reference
redis_settings = infra_settings.redis  # Redis settings reference
taskiq_settings = infra_settings.taskiq  # TaskIQ settings reference
rabbitmq_settings = infra_settings.rabbitmq  # RabbitMQ settings reference

