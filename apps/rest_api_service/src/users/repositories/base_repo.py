from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import Base
from sqlalchemy import select, update, delete
from fastapi_pagination.ext.sqlalchemy import paginate


Model = TypeVar('Model', bound=Base)

class BaseRepository(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession):
        self.model = model
        self.session = session

    async def create(self, **kwargs) -> Model:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: Model, **kwargs) -> Model | None:
        for key, value in kwargs.items():
            setattr(instance, key, value)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def delete(self,  id: int) -> None:
       await self.session.execute(
           delete(self.model).where(self.model.id == id)
       )
       await self.session.commit()

    async def get_all(self) -> list[Model]:
        result = await self.session.execute(select(self.model))
        return list(result.scalars().all())

    async def get_by_id(self, id: int) -> Model | None:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_all_paginated(self):
        """
        Ефективно отримує сторінку елементів.
        Розширення fastapi-pagination самостійно модифікує SQL-запит,
        додавши туди необхідні LIMIT та OFFSET, а також виконає швидкий COUNT.
        """
        query = select(self.model)
        # Просто передаємо сесію та сам об'єкт запиту (select)
        return await paginate(self.session, query)