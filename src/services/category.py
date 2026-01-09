from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.category import CategoryRepository
from src.schemas.category import CategoryCreate, CategoryUpdate
from src.exceptions.custom_exceptions import NotFoundException, AlreadyExistsException


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.repository = CategoryRepository(db)

    async def create_category(self, category: CategoryCreate) -> dict:
        existing = await self.repository.get_by_name(category.name)
        if existing:
            raise AlreadyExistsException(f"Category with name '{category.name}' already exists")

        db_category = await self.repository.create(**category.model_dump())
        return db_category

    async def get_category(self, pk_id: int) -> dict:
        category = await self.repository.get_by_id(pk_id)
        if not category:
            raise NotFoundException(f"Category with id {pk_id} not found")
        return category

    async def get_category_by_uuid(self, id: str) -> dict:
        category = await self.repository.get_by_uuid(id)
        if not category:
            raise NotFoundException(f"Category with uuid {id} not found")
        return category

    async def get_all_categories(self, skip: int = 0, limit: int = 100) -> List[dict]:
        return await self.repository.get_all(skip, limit)

    async def update_category(self, pk_id: int, category: CategoryUpdate) -> dict:
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Category with id {pk_id} not found")

        if category.name and category.name != existing["name"]:
            name_exists = await self.repository.get_by_name(category.name)
            if name_exists:
                raise AlreadyExistsException(f"Category with name '{category.name}' already exists")

        update_data = category.model_dump(exclude_unset=True)
        updated = await self.repository.update(pk_id, **update_data)
        return updated

    async def delete_category(self, pk_id: int) -> bool:
        existing = await self.repository.get_by_id(pk_id)
        if not existing:
            raise NotFoundException(f"Category with id {pk_id} not found")

        return await self.repository.delete(pk_id)