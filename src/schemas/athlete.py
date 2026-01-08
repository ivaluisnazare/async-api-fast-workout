from typing import Optional
from pydantic import BaseModel, ConfigDict
import uuid
from datetime import datetime


class AthleteBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    cpf: str
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    training_center_id: Optional[int] = None
    category_id: Optional[int] = None


class AthleteCreate(AthleteBase):
    pass


class AthleteUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    cpf: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    training_center_id: Optional[int] = None
    category_id: Optional[int] = None


class AthleteResponse(AthleteBase):
    pk_id: int
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None