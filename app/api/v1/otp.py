from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.otp import OTPRequest, OTPVerifyRequest
from app.services.otp_service import (
    generate_and_store_otp,
    verify_otp,
)


router = APIRouter(
    prefix="/otp",
    tags=["OTP"]
)


# ============================================================
# SEND OTP
# ============================================================

@router.post("/send-otp")
def send_otp(
    payload: OTPRequest,
    db: Session = Depends(get_db),
):
    """
    Generate OTP, send it through Brevo,
    and store it in the database.
    """

    try:

        generate_and_store_otp(
            db=db,
            email=payload.email,
        )

        return {
            "success": True,
            "message": "OTP sent successfully",
            "email": payload.email,
        }

    except Exception as e:

        print("========================================")
        print("OTP SEND ERROR")
        print("========================================")
        print(str(e))
        print("========================================")

        raise HTTPException(
            status_code=500,
            detail="Failed to send OTP email",
        )


# ============================================================
# VERIFY OTP
# ============================================================

@router.post("/verify-otp")
def verify_otp_api(
    payload: OTPVerifyRequest,
    db: Session = Depends(get_db),
):
    """
    Verify the OTP entered by the user.
    """

    success, message = verify_otp(
        db=db,
        email=payload.email,
        otp=payload.otp,
    )

    if not success:

        raise HTTPException(
            status_code=400,
            detail=message,
        )

    return {
        "success": True,
        "message": message,
    }