from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from shared.database import get_db

from src.schemas.training_center import (
    TrainingCenterCreate,
    TrainingCenterUpdate,
    TrainingCenterResponse
)
from src.services.training_center import TrainingCenterService

router = APIRouter(prefix="/training-centers", tags=["training-centers"])

@router.post("/", response_model=TrainingCenterResponse, status_code=status.HTTP_201_CREATED)
async def create_training_center(
    training_center: TrainingCenterCreate,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    return await service.create_training_center(training_center)

@router.get("/", response_model=List[TrainingCenterResponse])
async def get_training_centers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    return await service.get_all_training_centers(skip, limit)

@router.get("/{pk_id}", response_model=TrainingCenterResponse)
async def get_training_center(
    pk_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    return await service.get_training_center(pk_id)

@router.get("/uuid/{id}", response_model=TrainingCenterResponse)
async def get_training_center_by_uuid(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    return await service.get_training_center_by_uuid(id)

@router.put("/{pk_id}", response_model=TrainingCenterResponse)
async def update_training_center(
    pk_id: int,
    training_center: TrainingCenterUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    return await service.update_training_center(pk_id, training_center)

@router.delete("/{pk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_training_center(
    pk_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = TrainingCenterService(db)
    await service.delete_training_center(pk_id)
    return None