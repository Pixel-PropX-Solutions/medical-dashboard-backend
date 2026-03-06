from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.auth.models import PyObjectId

class ClinicBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    plan: str = "basic"

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

class ClinicInDB(ClinicBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
