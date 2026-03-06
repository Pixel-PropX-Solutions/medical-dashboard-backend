from fastapi import APIRouter, Depends, HTTPException, status
from app.services.models import ServiceCreate, ServiceUpdate, ServiceInDB
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=ServiceInDB, status_code=status.HTTP_201_CREATED)
async def create_service(service: ServiceCreate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    service_dict = service.model_dump()
    service_db = ServiceInDB(**service_dict, clinic_id=current_user.clinic_id)
    
    result = await db.services.insert_one(service_db.model_dump(by_alias=True, exclude=["id"]))
    created_service = await db.services.find_one({"_id": result.inserted_id})
    created_service["_id"] = str(created_service["_id"])
    return created_service

@router.get("/")
async def list_services(current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    services = await db.services.find({"clinic_id": current_user.clinic_id}).to_list(100)
    for s in services:
        s["_id"] = str(s["_id"])
    return services

@router.patch("/{id}", response_model=ServiceInDB)
async def update_service(id: str, service_update: ServiceUpdate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    update_data = {k: v for k, v in service_update.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
        
    result = await db.services.update_one(
        {"_id": ObjectId(id), "clinic_id": current_user.clinic_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Service not found or no changes made")
        
    updated = await db.services.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return updated
