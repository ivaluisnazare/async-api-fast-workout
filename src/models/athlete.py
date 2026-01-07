from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
import uuid
from src.models.base import BaseModel

class Athlete(BaseModel):
    __tablename__ = "athlete"

    id = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    age = Column(Integer)
    weight = Column(Float(10, 2))
    height = Column(Float(10, 2))
    sex = Column(String(1))

    training_center_id = Column(Integer, ForeignKey("training_center.pk_id"))
    category_id = Column(Integer, ForeignKey("category.pk_id"))

    training_center = relationship("TrainingCenter", backref="athletes")
    category = relationship("Category", backref="athletes")