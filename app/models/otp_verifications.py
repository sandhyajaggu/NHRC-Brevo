from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.db.base import Base

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String(255), index=True, nullable=False)

    otp = Column(String(6), nullable=False)

    purpose = Column(String(50), nullable=False)

    candidate_type = Column(String(30), nullable=True)

    is_verified = Column(Boolean, default=False)

    attempts = Column(Integer, default=0)

    expires_at = Column(DateTime(timezone=True), nullable=False)

    last_sent_at = Column(DateTime(timezone=True), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )