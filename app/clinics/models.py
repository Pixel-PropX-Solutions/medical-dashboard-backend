from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.auth.models import PyObjectId


import uuid

class ClinicDoctor(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    fee: int = 0
    specialization: Optional[str] = None


def normalize_clinic_doctors_data(clinic: Dict[str, Any]) -> Dict[str, Any]:
    doctors = clinic.get("doctors") or []
    normalized_doctors: List[Dict[str, Any]] = []

    for doctor in doctors:
        if not isinstance(doctor, dict):
            continue
        doctor_name = str(doctor.get("name", "")).strip()
        if not doctor_name:
            continue
        normalized_doctors.append(
            {
                "id": doctor.get("id") or str(uuid.uuid4()),
                "name": doctor_name,
                "fee": int(doctor.get("fee", 0) or 0),
                "specialization": doctor.get("specialization"),
            }
        )

    clinic["doctors"] = normalized_doctors
    return clinic


class ClinicBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    plan: str = "basic"
    logo_url: Optional[str] = None
    default_template_id: Optional[str] = None
    doctors: Optional[List[ClinicDoctor]] = Field(default_factory=list)


class ClinicCreate(ClinicBase):
    pass


class ClinicUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    logo_url: Optional[str] = None
    default_template_id: Optional[str] = None


class ClinicSettingsUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    logo_url: Optional[str] = None
    default_template_id: Optional[str] = None
    doctors: Optional[List[ClinicDoctor]] = None


class ClinicInDB(ClinicBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
