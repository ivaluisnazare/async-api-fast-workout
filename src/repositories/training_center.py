from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.training_center import TrainingCenter
from src.repositories.base import BaseRepository


class TrainingCenterRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(TrainingCenter, db)

    async def get_by_name(self, name: str) -> Optional[TrainingCenter]:
        result = await self.db.execute(
            select(TrainingCenter).where(TrainingCenter.name == name)
        )
        return result.scalar_one_or_none()

    async def get_by_owner(self, owner: str) -> List[TrainingCenter]:
        result = await self.db.execute(
            select(TrainingCenter).where(TrainingCenter.owner == owner)
        )
        return result.scalars().all()