from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid
from src.models.base import BaseModel


class TrainingCenter(BaseModel):
    __tablename__ = "training_center"

    id = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(20), nullable=False)
    address = Column(String(60))
    owner = Column(String(30))