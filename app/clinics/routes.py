from fastapi import APIRouter, Depends, HTTPException, status
from app.clinics.models import ClinicCreate, ClinicInDB, ClinicUpdate
from app.auth.dependencies import get_current_admin
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/clinics", tags=["Clinics"])

@router.post("/", response_model=ClinicInDB, status_code=status.HTTP_201_CREATED)
async def create_clinic(clinic: ClinicCreate, current_user = Depends(get_current_admin)):
    db = get_db()
    clinic_dict = clinic.model_dump()
    clinic_db = ClinicInDB(**clinic_dict)
    
    result = await db.clinics.insert_one(clinic_db.model_dump(by_alias=True, exclude=["id"]))
    created_clinic = await db.clinics.find_one({"_id": result.inserted_id})
    return created_clinic

@router.get("/")
async def list_clinics(current_user = Depends(get_current_admin)):
    db = get_db()
    clinics = await db.clinics.find().to_list(100)
    for clinic in clinics:
        clinic["_id"] = str(clinic["_id"])
    return clinics

@router.patch("/{clinic_id}", response_model=ClinicInDB)
async def update_clinic(clinic_id: str, clinic_update: ClinicUpdate, current_user = Depends(get_current_admin)):
    db = get_db()
    update_data = {k: v for k, v in clinic_update.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    result = await db.clinics.update_one(
        {"_id": ObjectId(clinic_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Clinic not found or no changes made")
        
    updated = await db.clinics.find_one({"_id": ObjectId(clinic_id)})
    return updated
