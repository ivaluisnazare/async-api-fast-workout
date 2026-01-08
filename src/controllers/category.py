from typing import List
from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from shared.database import get_db
from src.services.category import CategoryService
from src.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        return await service.create_category(category)


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        return await service.get_all_categories(skip, limit)

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category_by_id(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        return await service.get_category(category_id)


@router.get("/uuid/{category_uuid}", response_model=CategoryResponse)
async def get_category_by_uuid(
    category_uuid: str,
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        return await service.get_category_by_uuid(category_uuid)

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        return await service.update_category(category_id, category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
        service = CategoryService(db)
        await service.delete_category(category_id)
        return None
