"""Database configuration and session management module.

This module handles SQLAlchemy async engine creation and provides
database session management for the application using async patterns.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from infra.config.base_settings import get_infra_settings
from typing import AsyncGenerator

# Base class for all ORM models
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models.

    Inherits from DeclarativeBase for ORM mapping and MappedAsDataclass
    for dataclass-like behavior. All database models should inherit from this
    base class to ensure consistent configuration and behavior.
    """
    pass

# Get infrastructure settings
settings = get_infra_settings()
database_settings = settings.db



def get_async_engine():
    """Create and return async SQLAlchemy engine instance.

    Returns:
        AsyncEngine: Configured async database engine with echo settings
                    from database configuration.
    """
    return create_async_engine(
        database_settings.url,
        echo=database_settings.ECHO)


# Create async session factory for database connections
AsyncSessionLocal = async_sessionmaker(
    bind=get_async_engine(),
    class_=AsyncSession,
    expire_on_commit=False
)




# TODO: Implement database initialization function
# async def init_db():
#     """Initialize database tables and schema."""
#     # import models and create tables
