from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.athlete import Athlete
from src.repositories.base import BaseRepository


class AthleteRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(Athlete, db)

    async def get_by_cpf(self, cpf: str) -> Optional[Athlete]:
        result = await self.db.execute(
            select(Athlete).where(Athlete.cpf == cpf)
        )
        return result.scalar_one_or_none()

    async def get_by_training_center(self, training_center_id: int) -> List[Athlete]:
        result = await self.db.execute(
            select(Athlete).where(Athlete.training_center_id == training_center_id)
        )
        return result.scalars().all()

    async def get_by_category(self, category_id: int) -> List[Athlete]:
        result = await self.db.execute(
            select(Athlete).where(Athlete.category_id == category_id)
        )
        return result.scalars().all()

    async def get_by_age_range(self, min_age: int, max_age: int) -> List[Athlete]:
        result = await self.db.execute(
            select(Athlete).where(
                and_(Athlete.age >= min_age, Athlete.age <= max_age)
            )
        )
        return result.scalars().all()