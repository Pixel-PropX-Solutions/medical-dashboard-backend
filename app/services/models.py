from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.auth.models import PyObjectId

class ServiceBase(BaseModel):
    service_name: str
    price: float
    active: bool = True

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    price: Optional[float] = None
    active: Optional[bool] = None

class ServiceInDB(ServiceBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    clinic_id: str

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
