from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from datetime import datetime
from typing import Optional
import uuid

class BaseSchema(PydanticBaseModel):
    model_config = ConfigDict(from_attributes=True)

class BaseResponseSchema(BaseSchema):
    pk_id: int
    id: uuid.UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None