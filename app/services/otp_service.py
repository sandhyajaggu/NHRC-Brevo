from datetime import datetime, timedelta, timezone

from app.models.otp_verifications import OTPVerification
from app.services.brevo_service import send_otp_email
from app.utils.otp import generate_random_otp


# ============================================================
# GENERATE AND STORE OTP
# ============================================================

def generate_and_store_otp(
    db,
    email: str,
):
    """
    Generate OTP, send OTP email through Brevo,
    and store OTP information in database.
    """

    # --------------------------------------------------------
    # Generate OTP
    # --------------------------------------------------------

    otp = generate_random_otp()

    # --------------------------------------------------------
    # Current UTC time
    # --------------------------------------------------------

    current_time = datetime.now(timezone.utc)

    # OTP valid for 10 minutes
    expiry = current_time + timedelta(minutes=10)

    # --------------------------------------------------------
    # Check existing OTP record
    # --------------------------------------------------------

    otp_record = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == email
        )
        .first()
    )

    # --------------------------------------------------------
    # Update existing record
    # --------------------------------------------------------

    if otp_record:

        otp_record.otp = otp
        otp_record.expires_at = expiry
        otp_record.last_sent_at = current_time
        otp_record.is_verified = False
        otp_record.attempts = 0

    # --------------------------------------------------------
    # Create new record
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Send OTP email
    # --------------------------------------------------------

    try:

        email_sent = send_otp_email(
            email=email,
            otp=otp,
        )

        # Brevo service returns False when email fails
        if not email_sent:

            db.rollback()

            raise Exception(
                "Brevo failed to send OTP email"
            )

    except Exception:

        db.rollback()

        raise

    # --------------------------------------------------------
    # Email was successfully accepted
    # Store OTP in database
    # --------------------------------------------------------

    db.commit()

    return True


# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp(
    db,
    email: str,
    otp: str,
):
    """
    Verify OTP.
    """

    # --------------------------------------------------------
    # Find OTP record
    # --------------------------------------------------------

    otp_record = (
        db.query(OTPVerification)
        .filter(
            OTPVerification.email == email
        )
        .first()
    )

    # --------------------------------------------------------
    # OTP not found
    # --------------------------------------------------------

    if otp_record is None:

        return False, "OTP not found"

    # --------------------------------------------------------
    # Already verified
    # --------------------------------------------------------

    if otp_record.is_verified:

        return False, "OTP already verified"

    # --------------------------------------------------------
    # Check expiration
    # --------------------------------------------------------

    current_time = datetime.now(timezone.utc)

    if otp_record.expires_at < current_time:

        return False, "OTP expired"

    # --------------------------------------------------------
    # Check OTP
    # --------------------------------------------------------

    if otp_record.otp != otp:

        otp_record.attempts += 1

        db.commit()

        return False, "Invalid OTP"

    # --------------------------------------------------------
    # Mark verified
    # --------------------------------------------------------

    otp_record.is_verified = True

    db.commit()

    return True, "OTP verified successfully"