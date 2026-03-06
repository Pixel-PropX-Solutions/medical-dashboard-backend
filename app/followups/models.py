from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from app.auth.models import PyObjectId

class FollowupBase(BaseModel):
    patient_id: str
    next_visit_date: datetime
    notes: Optional[str] = None
    status: str = "pending" # pending, completed, cancelled

class FollowupCreate(FollowupBase):
    pass

class FollowupInDB(FollowupBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    clinic_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
