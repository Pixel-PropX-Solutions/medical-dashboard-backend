from fastapi import APIRouter, Depends, HTTPException, status
from app.billing.models import BillCreate, BillInDB
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
from bson import ObjectId

router = APIRouter(prefix="/bills", tags=["Billing"])

@router.post("/", response_model=BillInDB, status_code=status.HTTP_201_CREATED)
async def create_bill(bill: BillCreate, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    
    # Verify patient
    patient = await db.patients.find_one({
        "_id": ObjectId(bill.patient_id),
        "clinic_id": current_user.clinic_id
    })
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
        
    bill_dict = bill.model_dump()
    
    # Optional: recalculate total_amount server-side for security
    calculated_total = sum(item["price"] * item["quantity"] for item in bill_dict["services"])
    bill_dict["total_amount"] = calculated_total
    
    bill_db = BillInDB(**bill_dict, clinic_id=current_user.clinic_id)
    
    result = await db.bills.insert_one(bill_db.model_dump(by_alias=True, exclude=["id"]))
    created_bill = await db.bills.find_one({"_id": result.inserted_id})
    created_bill["_id"] = str(created_bill["_id"])
    return created_bill

@router.get("/{id}")
async def get_bill(id: str, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    item = await db.bills.find_one({"_id": ObjectId(id), "clinic_id": current_user.clinic_id})
    if not item:
        raise HTTPException(status_code=404, detail="Bill not found")
    item["_id"] = str(item["_id"])
    return item
