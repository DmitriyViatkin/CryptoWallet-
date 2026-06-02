"""Settings configuration for the User service application.

This module defines application-specific settings for the CryptoWallet
REST API service including JWT authentication parameters and service metadata.
"""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from .infra.config.base_settings import (
    BaseInfraSettings,
    InfraSettings,
    get_infra_settings,
)


class RestAPIServiceSettings(BaseInfraSettings):
    """REST API service configuration settings.

    Defines all configuration parameters for the CryptoWallet authentication
    service including JWT settings, service metadata, and infrastructure settings.
    Environment variables are loaded from .env file with AUTH_ prefix.
    """
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parents[2] / ".env"),
        env_prefix="AUTH_",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Service metadata
    TITLE: str = "CryptoWallet — auth service"
    DESCRIPTION: str = "JWT auth, registration, permissions"
    DEBUG: bool = False
    BASE_URL: str = Field(default="http://localhost:8001")

    # JWT authentication settings
    # NOTE: a default development secret is provided so the app can start
    # without an external .env. Replace with a secure value in production
    # by setting AUTH_SECRET_KEY in your environment or .env file.
    SECRET_KEY: str = Field(default="dev-secret")  # Secret key for signing JWT tokens
    ALGORITHM: str = "HS256"  # Hashing algorithm for JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Access token lifetime in minutes
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # Refresh token lifetime in days

    # Infrastructure settings (database, redis, etc.)
    infra: InfraSettings = Field(default_factory=get_infra_settings)


@lru_cache
def get_settings() -> RestAPIServiceSettings:
    """Get cached REST API service settings instance.

    Returns:
        RestAPIServiceSettings: Singleton instance of service settings.
                               Cached to prevent repeated initialization.
    """
    return RestAPIServiceSettings()


# Global settings instance
auth_settings: RestAPIServiceSettings = get_settings()

