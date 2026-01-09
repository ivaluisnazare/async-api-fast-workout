from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.athlete import AthleteRepository
from src.schemas.athlete import AthleteCreate, AthleteUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


class AthleteService:
    def __init__(self, db: AsyncSession):
        self.repository = AthleteRepository(db)

    async def create_athlete(self, athlete: AthleteCreate) -> dict:
        # Check if athlete with same CPF exists
        existing = await self.repository.get_by_cpf(athlete.cpf)
        if existing:
            raise AlreadyExistsException(f"Athlete with CPF '{athlete.cpf}' already exists")

        db_athlete = await self.repository.create(**athlete.model_dump())
        return db_athlete

    async def get_athlete(self, pk_id: int) -> dict:
        athlete = await self.repository.get_by_id(pk_id)
        if not athlete:
            raise NotFoundException(f"Athlete with id {pk_id} not found")
        return athlete

    async def get_athlete_by_uuid(self, id: str) -> dict:
        athlete = await self.repository.get_by_uuid(id)
        if not athlete:
            raise NotFoundException(f"Athlete with uuid {id} not found")
        return athlete

    async def get_all_athletes(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return await self.repository.get_all(skip, limit)

    async def update_athlete(self, pk_id: int, athlete: AthleteUpdate) -> dict:
        # Check if athlete exists
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Athlete with id {pk_id} not found")

        # If CPF is being updated, check for conflicts
        if athlete.cpf and athlete.cpf != existing["cpf"]:
            cpf_exists = await self.repository.get_by_cpf(athlete.cpf)
            if cpf_exists:
                raise AlreadyExistsException(f"Athlete with CPF '{athlete.cpf}' already exists")

        update_data = athlete.model_dump(exclude_unset=True)
        updated = await self.repository.update(pk_id, **update_data)
        return updated

    async def delete_athlete(self, pk_id: int) -> bool:
        # Check if athlete exists
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Athlete with id {pk_id} not found")

        return await self.repository.delete(pk_id)

    async def get_athletes_by_training_center(self, training_center_id: int) -> List[dict]:
        return await self.repository.get_by_training_center(training_center_id)

    async def get_athletes_by_category(self, category_id: int) -> List[dict]:
        return await self.repository.get_by_category(category_id)

    async def get_athletes_by_age_range(self, min_age: int, max_age: int) -> List[dict]:
        return await self.repository.get_by_age_range(min_age, max_age)