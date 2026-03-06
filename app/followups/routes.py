from fastapi import APIRouter, Depends, HTTPException, status
from app.followups.models import FollowupCreate, FollowupInDB
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/followups", tags=["Follow-Ups"])

@router.post("/", response_model=FollowupInDB, status_code=status.HTTP_201_CREATED)
async def create_followup(followup: FollowupCreate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    
    # Verify patient
    patient = await db.patients.find_one({
        "_id": ObjectId(followup.patient_id),
        "clinic_id": current_user.clinic_id
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    followup_dict = followup.model_dump()
    followup_db = FollowupInDB(**followup_dict, clinic_id=current_user.clinic_id)
    
    result = await db.followups.insert_one(followup_db.model_dump(by_alias=True, exclude=["id"]))
    created_followup = await db.followups.find_one({"_id": result.inserted_id})
    created_followup["_id"] = str(created_followup["_id"])
    return created_followup

@router.get("/")
async def list_followups(current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    # E.g. fetch pending followups
    items = await db.followups.find({
        "clinic_id": current_user.clinic_id,
        "status": "pending"
    }).sort("next_visit_date", 1).to_list(100)
    
    for item in items:
        item["_id"] = str(item["_id"])
    return items
