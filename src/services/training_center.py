from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.training_center import TrainingCenterRepository
from src.schemas.training_center import TrainingCenterCreate, TrainingCenterUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


class TrainingCenterService:
    def __init__(self, db: AsyncSession):
        self.repository = TrainingCenterRepository(db)

    async def create_training_center(self, training_center: TrainingCenterCreate) -> dict:
        # Check if training center with same name exists
        existing = await self.repository.get_by_name(training_center.name)
        if existing:
            raise AlreadyExistsException(f"Training center with name '{training_center.name}' already exists")

        db_training_center = await self.repository.create(**training_center.model_dump())
        return db_training_center

    async def get_training_center(self, pk_id: int) -> dict:
        training_center = await self.repository.get_by_id(pk_id)
        if not training_center:
            raise NotFoundException(f"Training center with id {pk_id} not found")
        return training_center

    async def get_training_center_by_uuid(self, id: str) -> dict:
        training_center = await self.repository.get_by_uuid(id)
        if not training_center:
            raise NotFoundException(f"Training center with uuid {id} not found")
        return training_center

    async def get_all_training_centers(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return await self.repository.get_all(skip, limit)

    async def update_training_center(self, pk_id: int, training_center: TrainingCenterUpdate) -> dict:
        # Check if training center exists
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Training center with id {pk_id} not found")

        # If name is being updated, check for conflicts
        if training_center.name and training_center.name != existing.name:
            name_exists = await self.repository.get_by_name(training_center.name)
            if name_exists:
                raise AlreadyExistsException(f"Training center with name '{training_center.name}' already exists")

        update_data = training_center.model_dump(exclude_unset=True)
        updated = await self.repository.update(pk_id, **update_data)
        return updated

    async def delete_training_center(self, pk_id: int) -> bool:
        # Check if training center exists
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Training center with id {pk_id} not found")

        return await self.repository.delete(pk_id)