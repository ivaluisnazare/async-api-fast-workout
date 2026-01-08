#category.py
from sqlalchemy import Column, String, UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from src.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "category"

    id = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(20), unique=True, nullable=False)