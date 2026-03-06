from fastapi import APIRouter, Depends, HTTPException, Response
from app.auth.dependencies import get_current_clinic_user
from app.auth.models import TokenData
from app.database import get_db
from app.pdf.pdf_generator import generate_pdf
from bson import ObjectId
from jinja2 import Template

router = APIRouter(prefix="/pdf", tags=["PDF Generation"])

@router.get("/bill/{bill_id}")
async def generate_bill_pdf(bill_id: str, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    # 1. Fetch Bill
    bill = await db.bills.find_one({"_id": ObjectId(bill_id), "clinic_id": current_user.clinic_id})
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
        
    # 2. Fetch Patient & Clinic Info
    patient = await db.patients.find_one({"_id": ObjectId(bill["patient_id"])})
    clinic = await db.clinics.find_one({"_id": ObjectId(current_user.clinic_id)})
    
    # 3. Fetch HTML Template
    template_doc = await db.templates.find_one({
        "clinic_id": current_user.clinic_id, 
        "template_type": "invoice"
    })
    
    if not template_doc:
        raise HTTPException(status_code=400, detail="No invoice template found for clinic")
        
    # 4. Inject Dynamic Data
    jinja_template = Template(template_doc["html_content"])
    
    # Format services as HTML rows for simplicity in templating, or pass the raw list
    services_html = "".join([f"<tr><td>{s['service_name']}</td><td>{s['price']}</td></tr>" for s in bill["services"]])
    
    rendered_html = jinja_template.render(
        clinic_name=clinic.get("name", ""),
        patient_name=patient.get("name", ""),
        phone=patient.get("phone", ""),
        services=services_html,
        total=bill["total_amount"]
    )
    
    # 5. Generate PDF
    pdf_bytes = await generate_pdf(rendered_html, format_type="A4")
    
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=invoice_{bill_id}.pdf"}
    )
    
@router.get("/parchi/{visit_id}")
async def generate_parchi_pdf(visit_id: str, current_user: TokenData = Depends(get_current_clinic_user)):
    db = get_db()
    # 1. Fetch Visit
    visit = await db.visits.find_one({"_id": ObjectId(visit_id), "clinic_id": current_user.clinic_id})
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
        
    patient = await db.patients.find_one({"_id": ObjectId(visit["patient_id"])})
    clinic = await db.clinics.find_one({"_id": ObjectId(current_user.clinic_id)})
    
    template_doc = await db.templates.find_one({
        "clinic_id": current_user.clinic_id, 
        "template_type": "medical_parchi"
    })
    
    if not template_doc:
        raise HTTPException(status_code=400, detail="No medical parchi template found for clinic")
        
    # Inject Data
    jinja_template = Template(template_doc["html_content"])
    
    rendered_html = jinja_template.render(
        clinic_name=clinic.get("name", ""),
        patient_name=patient.get("name", ""),
        phone=patient.get("phone", ""),
        diagnosis=visit.get("diagnosis", ""),
        notes=visit.get("doctor_notes", ""),
        medicines="<br>".join(visit.get("medicines", []))
    )
    
    pdf_bytes = await generate_pdf(rendered_html, format_type="receipt")
    
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=parchi_{visit_id}.pdf"}
    )
