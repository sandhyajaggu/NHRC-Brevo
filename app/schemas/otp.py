from pydantic import BaseModel, EmailStr


# ============================================================
# SEND OTP REQUEST
# ============================================================

class OTPRequest(BaseModel):
    email: EmailStr


# ============================================================
# VERIFY OTP REQUEST
# ============================================================

class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str