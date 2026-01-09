#repository for Category model
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.category import Category
from src.repositories.base import BaseRepository


class CategoryRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Category, db)

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self.db.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()