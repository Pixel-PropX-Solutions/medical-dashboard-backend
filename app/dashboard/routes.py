from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
from datetime import datetime, time

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
async def get_dashboard_stats(current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    
    # Calculate "today" range
    today_start = datetime.combine(datetime.utcnow().date(), time.min)
    today_end = datetime.combine(datetime.utcnow().date(), time.max)
    
    # 1. Total patients today
    patients_today = await db.patients.count_documents({
        "clinic_id": current_user.clinic_id,
        "first_visit_date": {"$gte": today_start, "$lte": today_end}
    })
    
    # 2. Total revenue today
    bills_today = await db.bills.find({
        "clinic_id": current_user.clinic_id,
        "created_at": {"$gte": today_start, "$lte": today_end}
    }).to_list(100)
    
    total_revenue = sum(b.get("total_amount", 0) for b in bills_today)
    
    # 3. Repeat patients
    # Patients with visit_count > 1
    repeat_patients = await db.patients.count_documents({
        "clinic_id": current_user.clinic_id,
        "visit_count": {"$gt": 1}
    })
    
    # 4. Total visits today
    total_visits = await db.visits.count_documents({
        "clinic_id": current_user.clinic_id,
        "created_at": {"$gte": today_start, "$lte": today_end}
    })
    
    return {
        "patients_today": patients_today,
        "total_revenue": total_revenue,
        "repeat_patients": repeat_patients,
        "total_visits": total_visits
    }
