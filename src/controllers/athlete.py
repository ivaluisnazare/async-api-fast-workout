from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from shared.database import get_db
from src.schemas.athlete import (
    AthleteCreate,
    AthleteUpdate,
    AthleteResponse
)
from src.services.athlete import AthleteService

router = APIRouter(prefix="/athletes", tags=["athletes"])

@router.post("/", response_model=AthleteResponse, status_code=status.HTTP_201_CREATED)
async def create_athlete(
    athlete: AthleteCreate,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.create_athlete(athlete)

@router.get("/", response_model=List[AthleteResponse])
async def get_athletes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.get_all_athletes(skip, limit)

@router.get("/{pk_id}", response_model=AthleteResponse)
async def get_athlete(
    pk_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.get_athlete(pk_id)

@router.get("/uuid/{id}", response_model=AthleteResponse)
async def get_athlete_by_uuid(
    id: str,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.get_athlete_by_uuid(id)

@router.put("/{pk_id}", response_model=AthleteResponse)
async def update_athlete(
    pk_id: int,
    athlete: AthleteUpdate,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.update_athlete(pk_id, athlete)

@router.delete("/{pk_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_athlete(
    pk_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    await service.delete_athlete(pk_id)
    return None

@router.get("/training-center/{training_center_id}", response_model=List[AthleteResponse])
async def get_athletes_by_training_center(
    training_center_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.get_athletes_by_training_center(training_center_id)

@router.get("/category/{category_id}", response_model=List[AthleteResponse])
async def get_athletes_by_category(
    category_id: int,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    return await service.get_athletes_by_category(category_id)

@router.get("/age-range/{min_age}/{max_age}", response_model=List[AthleteResponse])
async def get_athletes_by_age_range(
    min_age: int,
    max_age: int,
    db: AsyncSession = Depends(get_db)
):
    service = AthleteService(db)
    if min_age > max_age:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_age must be less than or equal to max_age"
        )
    return await service.get_athletes_by_age_range(min_age, max_age)