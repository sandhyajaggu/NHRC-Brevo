from datetime import datetime, timedelta, timezone
from app.repositories.employee_repository import EmployeeRepository
from app.services.brevo_service import send_otp_email
from app.utils.otp import generate_random_otp


# ============================================================
# GENERATE OTP
# ============================================================

def generate_and_store_otp(db, email):

    employee = EmployeeRepository.get_by_email(db, email)

    if not employee:
        raise Exception("Employee not found")

    otp = generate_random_otp()

    current_time = datetime.now(timezone.utc)

    employee.email_otp = otp
    employee.otp_expiry = current_time + timedelta(minutes=10)
    employee.otp_verified = False
    employee.otp_attempts = 0
    employee.last_otp_sent = current_time

    db.commit()
    db.refresh(employee)

    send_otp_email(
        email=email,
        otp=otp,
    )

    return True


# ============================================================
# VERIFY OTP
# ============================================================

def verify_otp(db, email, otp):

    employee = EmployeeRepository.get_by_email(db, email)

    if not employee:
        return False, "Employee not found"

    if employee.email_otp != otp:
        employee.otp_attempts = (employee.otp_attempts or 0) + 1
        db.commit()
        return False, "Invalid OTP"

    if employee.otp_expiry is None:
        return False, "OTP not found"

    current_time = datetime.now(timezone.utc)

    if employee.otp_expiry < current_time:
        employee.email_otp = None
        employee.otp_expiry = None
        db.commit()
        return False, "OTP expired"

    employee.otp_verified = True
    employee.email_otp = None
    employee.otp_expiry = None
    employee.otp_attempts = 0
    employee.last_otp_sent = None

    db.commit()

    return True, "OTP verified successfully"