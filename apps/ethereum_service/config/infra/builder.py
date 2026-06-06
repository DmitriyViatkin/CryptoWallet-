from typing import Callable
from contextlib import AbstractAsyncContextManager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka


class FastAPIBuilder:
    """FastAPI builder"""

    def __init__(
        self,
        title: str,
        description: str,
        lifespan: Callable[[FastAPI], AbstractAsyncContextManager[None]] | None = None,
    ):
        """Initialize builder"""
        self.app: FastAPI = self.build_app(title, description, lifespan)
        self.register_di_container()

    @staticmethod
    def build_app(
        title: str,
        description: str,
        lifespan: Callable[[FastAPI], AbstractAsyncContextManager[None]] | None = None,
    ) -> FastAPI:
        """Build FastAPI app."""
        options: dict = {}

        app = FastAPI(
            title=title,
            version="0.0.1",
            openapi_tags=[],
            description=description,
            lifespan=lifespan,
            **options,
        )
        return app

    def get_app(self) -> FastAPI:
        """Return FastAPI app instance"""
        return self.app

    def register_di_container(self) -> None:
        """Inject dependencies into FastAPI"""
        from config.ioc import container
        setup_dishka(container=container, app=self.app)