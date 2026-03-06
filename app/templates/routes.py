from fastapi import APIRouter, Depends, HTTPException, status
from app.templates.models import TemplateCreate, TemplateUpdate, TemplateInDB
from app.auth.dependencies import get_current_clinic_user, get_current_admin
from app.auth.models import TokenData
from app.database import get_db
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/templates", tags=["Templates"])

@router.post("/", response_model=TemplateInDB, status_code=status.HTTP_201_CREATED)
async def create_template(template: TemplateCreate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    template_dict = template.model_dump()
    template_db = TemplateInDB(**template_dict, clinic_id=current_user.clinic_id)
    
    result = await db.templates.insert_one(template_db.model_dump(by_alias=True, exclude=["id"]))
    created = await db.templates.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])
    return created

@router.get("/")
async def list_templates(current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    items = await db.templates.find({"clinic_id": current_user.clinic_id}).to_list(100)
    for i in items:
        i["_id"] = str(i["_id"])
    return items

@router.patch("/{id}", response_model=TemplateInDB)
async def update_template(id: str, template_update: TemplateUpdate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    update_data = {k: v for k, v in template_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.templates.update_one(
        {"_id": ObjectId(id), "clinic_id": current_user.clinic_id},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")
        
    updated = await db.templates.find_one({"_id": ObjectId(id)})
    updated["_id"] = str(updated["_id"])
    return updated

@router.delete("/{id}")
async def delete_template(id: str, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    result = await db.templates.delete_one({"_id": ObjectId(id), "clinic_id": current_user.clinic_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Template not found")
    return {"detail": "Template deleted"}
