"""PostgreSQL database provider for dependency injection.

This module defines the Dishka provider for PostgreSQL database connections
using async SQLAlchemy session management.
"""

from dishka import Provider, Scope, provide
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    AsyncEngine,create_async_engine)

from  config.infra.config.base_settings import InfraSettings


class PostgresProvider(Provider):
    """Provides PostgreSQL database connections via dependency injection.

    Creates and manages async SQLAlchemy sessions at APP and REQUEST scopes.
    Uses Dishka framework for dependency injection.
    """
    @provide(scope=Scope.APP)
    async def provide_engine(self, infra_settings: InfraSettings
                             )-> AsyncGenerator[AsyncEngine, None]:
        """Create async SQLAlchemy engine for PostgreSQL.

        Creates a database engine at APP scope - instantiated once per application
        lifetime and reused for all requests.

        Args:
            infra_settings: Infrastructure configuration containing database settings.
        Returns:
            AsyncEngine: Configured async database engine for PostgreSQL.
        """
        engine= create_async_engine(
            infra_settings.db.url,
            echo=infra_settings.db.ECHO,
            pool_size=infra_settings.db.POOL_SIZE,
            max_overflow=infra_settings.db.POOL_MAX_OVERFLOW,
            pool_pre_ping=infra_settings.db.POOL_PRE_PING,
        )
        yield engine

        await engine.dispose()

    @provide(scope=Scope.APP)
    def provide_session_marker(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """Create async session factory from database engine.

        Creates a session maker at APP scope - instantiated once per application
        lifetime and reused for all requests.

        Args:
            engine: Configured async database engine.

        Returns:
            async_sessionmaker[AsyncSession]: Session factory for creating new sessions.
        """
        return async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False
        )

    @provide(scope=Scope.REQUEST)
    async def provide_session(self, session_marker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
        """Provide database session for individual request.

        Creates new session at REQUEST scope - instantiated once per HTTP request
        and automatically closed after request completes.

        Args:
            session_marker: Session factory from provide_session_marker.

        Yields:
            AsyncSession: Active database session for the request.
                         Automatically closed when the context exits.
        """
        async with session_marker() as session:
            yield session

