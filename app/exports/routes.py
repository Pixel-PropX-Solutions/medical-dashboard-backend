from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
import pandas as pd
import io

router = APIRouter(prefix="/export", tags=["Exports"])

@router.get("/patients")
async def export_patients(
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    current_user: TokenData = Depends(get_current_clinic_user)
):
    db = get_db()
    patients_cursor = db.patients.find({"clinic_id": current_user.clinic_id}, {"_id": 0, "clinic_id": 0})
    patients = await patients_cursor.to_list(length=None)
    
    df = pd.DataFrame(patients)
    
    if format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=patients.csv"
        return response
    else:
        stream = io.BytesIO()
        df.to_excel(stream, index=False, engine='openpyxl')
        stream.seek(0)
        response = StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = "attachment; filename=patients.xlsx"
        return response

@router.get("/bills")
async def export_bills(
    format: str = Query("csv", regex="^(csv|xlsx)$"),
    current_user: TokenData = Depends(get_current_clinic_user)
):
    db = get_db()
    bills_cursor = db.bills.find({"clinic_id": current_user.clinic_id}, {"_id": 0, "clinic_id": 0, "services": 0})
    bills = await bills_cursor.to_list(length=None)
    
    df = pd.DataFrame(bills)
    
    if format == "csv":
        stream = io.StringIO()
        df.to_csv(stream, index=False)
        response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=bills.csv"
        return response
    else:
        stream = io.BytesIO()
        df.to_excel(stream, index=False, engine='openpyxl')
        stream.seek(0)
        response = StreamingResponse(stream, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response.headers["Content-Disposition"] = "attachment; filename=bills.xlsx"
        return response
