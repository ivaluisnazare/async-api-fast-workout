from typing import Optional
from src.schemas.base import BaseResponseSchema

class CategoryBase(BaseResponseSchema):
    name: str

class CategoryCreate(BaseResponseSchema):
    name: str

class CategoryUpdate(BaseResponseSchema):
    name: Optional[str] = None

class CategoryResponse(CategoryBase):
    pass