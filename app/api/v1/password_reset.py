from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.member import Member

from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ResetPasswordRequest
)

from app.services.brevo_service import send_reset_password_email
from app.utils.otp import generate_random_otp

router = APIRouter(
    prefix="/password",
    tags=["Password Reset"]
)


@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    user = db.query(Member).filter(
        Member.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    
    reset_token = generate_random_otp()

    send_reset_password_email(
        email=email,
        otp=reset_token
    )

    return {
        "message": "Password reset email sent successfully"
    }


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest
):
    return {
        "message": "Password updated successfully"
    }