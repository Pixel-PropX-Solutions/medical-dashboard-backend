from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.auth.models import PyObjectId


class ClinicDoctor(BaseModel):
    name: str
    fee: int = 0


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
                "name": doctor_name,
                "fee": int(doctor.get("fee", 0) or 0),
            }
        )

    if not normalized_doctors:
        legacy_name = str(clinic.get("default_doctor_name", "")).strip()
        if legacy_name:
            normalized_doctors.append(
                {
                    "name": legacy_name,
                    "fee": int(clinic.get("default_doctor_fee", 0) or 0),
                }
            )

    clinic["doctors"] = normalized_doctors

    if normalized_doctors:
        if not clinic.get("default_doctor_name"):
            clinic["default_doctor_name"] = normalized_doctors[0]["name"]
        if clinic.get("default_doctor_fee") is None:
            clinic["default_doctor_fee"] = normalized_doctors[0]["fee"]

    return clinic


class ClinicBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    plan: str = "basic"
    logo_url: Optional[str] = None
    default_template_id: Optional[str] = None
    default_doctor_name: Optional[str] = None
    default_doctor_fee: Optional[int] = 0
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
    default_doctor_name: Optional[str] = None
    default_doctor_fee: Optional[int] = 0
    doctors: Optional[List[ClinicDoctor]] = None


class ClinicInDB(ClinicBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
