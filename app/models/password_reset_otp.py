from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base


class PasswordResetOTP(Base):
    __tablename__ = "password_reset_otps"

    id = Column(Integer, primary_key=True, index=True)

    # Lower-cased member email; one active reset OTP per email
    email = Column(String(255), unique=True, index=True, nullable=False)

    # bcrypt hash of the OTP (the plain OTP is only sent by email)
    otp_hash = Column(String(255), nullable=False)

    is_used = Column(Boolean, nullable=False, default=False)

    attempts = Column(Integer, nullable=False, default=0)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
