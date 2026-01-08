from typing import TypeVar, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.models.base import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseRepository:
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def create(self, **kwargs) -> ModelType:
        db_obj = self.model(**kwargs)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def get_by_id(self, pk_id: int) -> Optional[ModelType]:
        result = await self.db.execute(
            select(self.model).where(self.model.pk_id == pk_id)
        )
        return result.scalar_one_or_none()

    async def get_by_uuid(self, id: str) -> Optional[ModelType]:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def update(self, pk_id: int, **kwargs) -> Optional[ModelType]:
        await self.db.execute(
            update(self.model)
            .where(self.model.pk_id == pk_id)
            .values(**kwargs)
        )
        await self.db.commit()
        return await self.get_by_id(pk_id)

    async def delete(self, pk_id: int) -> bool:
        await self.db.execute(
            delete(self.model).where(self.model.pk_id == pk_id)
        )
        await self.db.commit()
        return True

    async def exists(self, pk_id: int) -> bool:
        result = await self.db.execute(
            select(self.model).where(self.model.pk_id == pk_id)
        )
        return result.scalar_one_or_none() is not None