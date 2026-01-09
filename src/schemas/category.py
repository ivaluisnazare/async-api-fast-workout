#schemas for Category entity
from typing import Optional
from pydantic import BaseModel
from src.schemas.base import BaseResponseSchema

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = None

class CategoryResponse(BaseResponseSchema):
    name: str
