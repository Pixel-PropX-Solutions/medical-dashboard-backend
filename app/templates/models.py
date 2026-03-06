from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.auth.models import PyObjectId

class TemplateBase(BaseModel):
    template_name: str
    template_type: str # invoice, medical_parchi, receipt
    html_content: str
    
class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    template_name: Optional[str] = None
    template_type: Optional[str] = None
    html_content: Optional[str] = None

class TemplateInDB(TemplateBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    clinic_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
