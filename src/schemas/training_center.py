from typing import Optional
from src.schemas.base import BaseSchema, BaseResponseSchema

class TrainingCenterBase(BaseSchema):
    name: str
    address: Optional[str] = None
    owner: Optional[str] = None

class TrainingCenterCreate(TrainingCenterBase):
    pass

class TrainingCenterUpdate(BaseSchema):
    name: Optional[str] = None
    address: Optional[str] = None
    owner: Optional[str] = None

class TrainingCenterResponse(TrainingCenterBase, BaseResponseSchema):
    pass