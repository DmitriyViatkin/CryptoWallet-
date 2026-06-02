from typing import TypeVar, Generic
from src.users.repositories.base_repo import BaseRepository

Model = TypeVar('Model')

class BaseService(Generic[Model]):

    def __init__(self, repository: BaseRepository[Model]):
        self._repo = repository

    async def get_by_id(self, id: int) -> Model | None:
        return await self._repo.get_by_id(id)

    async def get_all(self) -> list[Model]:
        return await self._repo.get_all()

    async def update(self, instance: Model, **kwargs) -> Model | None:
        return await self._repo.update(instance, **kwargs)

    async def delete(self, id: int) -> None:
        await self._repo.delete(id)



