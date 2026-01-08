from typing import Optional
from src.schemas.base import BaseResponseSchema

class AthleteBase(BaseResponseSchema):
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

class AthleteUpdate(BaseResponseSchema):
    name: Optional[str] = None
    cpf: Optional[str] = None
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    sex: Optional[str] = None
    training_center_id: Optional[int] = None
    category_id: Optional[int] = None

class AthleteResponse(AthleteBase):
    pass