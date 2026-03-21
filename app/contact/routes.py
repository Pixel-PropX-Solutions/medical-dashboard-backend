from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

from app.config import settings
from app.utils.mail_module import template
from app.utils.mail_module import mail

router = APIRouter(prefix="/contact", tags=["Contact"])


class ContactQuery(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120, alias="fullName")
    phone_number: str = Field(..., min_length=7, max_length=25, alias="phoneNumber")
    email: EmailStr
    message_type: str = Field(..., min_length=2, max_length=50, alias="messageType")
    message: str = Field(..., min_length=5, max_length=4000)


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def submit_contact_query(
    payload: ContactQuery, background_tasks: BackgroundTasks
):
    admin_email = settings.SMTP_USERNAME
    if not admin_email:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Contact email is not configured on the server",
        )

    background_tasks.add_task(
        mail.send,
        "New User Query - Clinova",
        admin_email,
        template.QueryEmail(
            fullName=payload.full_name,
            email=payload.email,
            phone=payload.phone_number,
            message=payload.message,
            messageType=payload.message_type,
        ),
    )

    return {"message": "Your query has been submitted successfully"}
