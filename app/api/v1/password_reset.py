from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hash_password, verify_password
from app.models.member import Member
from app.models.password_reset_otp import PasswordResetOTP

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

OTP_EXPIRY_MINUTES = 10
MAX_OTP_ATTEMPTS = 5


def get_member_by_email(db: Session, email: str):
    return db.query(Member).filter(
        func.lower(Member.email) == email.strip().lower()
    ).first()


@router.post("/forgot-password")
def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):

    user = get_member_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # ==========================================
    # SAVE OTP (replaces any earlier reset OTP)
    # ==========================================

    otp = generate_random_otp()

    reset_email = user.email.strip().lower()

    otp_record = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.email == reset_email
    ).first()

    if not otp_record:
        otp_record = PasswordResetOTP(email=reset_email)
        db.add(otp_record)

    otp_record.otp_hash = hash_password(otp)
    otp_record.is_used = False
    otp_record.attempts = 0
    otp_record.expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=OTP_EXPIRY_MINUTES
    )

    # ==========================================
    # SEND EMAIL
    # ==========================================

    email_sent = send_reset_password_email(
        email=user.email,
        otp=otp
    )

    if not email_sent:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to send password reset email"
        )

    db.commit()

    return {
        "message": "Password reset email sent successfully"
    }


@router.post("/reset-password")
def reset_password(
    payload: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    if payload.new_password != payload.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    user = get_member_by_email(db, payload.email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # ==========================================
    # VERIFY OTP
    # ==========================================

    otp_record = db.query(PasswordResetOTP).filter(
        PasswordResetOTP.email == user.email.strip().lower()
    ).first()

    if not otp_record:
        raise HTTPException(
            status_code=400,
            detail="OTP not found. Please request a new OTP"
        )

    if otp_record.is_used:
        raise HTTPException(
            status_code=400,
            detail="OTP already used. Please request a new OTP"
        )

    expires_at = otp_record.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=400,
            detail="OTP expired. Please request a new OTP"
        )

    if otp_record.attempts >= MAX_OTP_ATTEMPTS:
        raise HTTPException(
            status_code=400,
            detail="Too many wrong attempts. Please request a new OTP"
        )

    if not verify_password(payload.otp, otp_record.otp_hash):
        otp_record.attempts += 1
        db.commit()

        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )

    # ==========================================
    # UPDATE PASSWORD
    # ==========================================

    user.password_hash = hash_password(payload.new_password)

    otp_record.is_used = True

    db.commit()

    return {
        "message": "Password updated successfully"
    }
