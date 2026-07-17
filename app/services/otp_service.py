from datetime import datetime, timedelta, timezone
from app.models.otp_verifications import OTPVerification
from app.repositories.employee_repository import EmployeeRepository
from app.services.brevo_service import send_otp_email
from app.utils.otp import  generate_random_otp, verify_value


# ============================================================
# GENERATE OTP
# ============================================================

def generate_and_store_otp(
    db,
    email: str,
    
):

    otp = generate_random_otp()

    current_time = datetime.now(timezone.utc)

    expiry = current_time + timedelta(minutes=10)

    otp_record = db.query(
        OTPVerification
    ).filter(
        OTPVerification.email == email
    ).first()

    if otp_record:

        otp_record.otp = otp
        otp_record.expires_at = expiry
        otp_record.last_sent_at = current_time
        otp_record.is_verified = False
        otp_record.attempts = 0

    else:

        otp_record = OTPVerification(
            email=email,
            otp=otp,
            expires_at=expiry,
            last_sent_at=current_time,
            attempts=0,
            is_verified=False,
        )

        db.add(otp_record)

    db.commit()

    send_otp_email(
        email=email,
        otp=otp,
    )

    return True

# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp(db, email, otp):

    otp_record = (
    db.query(OTPVerification)
    .filter(
        OTPVerification.email == email
    )
    .first()
)

    if otp_record is None:
        return False, "OTP not found"

    if otp_record.is_verified:
        return False, "OTP already verified"

    if otp_record.otp != otp:
        otp_record.attempts += 1
        db.commit()
        return False, "Invalid OTP"

    if otp_record.expires_at < datetime.now(timezone.utc):
        return False, "OTP expired"

    otp_record.is_verified = True
    db.commit()

    return True, "OTP verified successfully"