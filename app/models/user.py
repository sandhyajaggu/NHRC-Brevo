from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from datetime import datetime
from app.db.base import Base
import enum


class UserRole(str, enum.Enum):
    admin = "admin"
    employee = "employee"
    student = "student"
    representative = "representative"
    member = "member"
    tpo = "tpo"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False, index=True)

    mobile = Column(String, unique=True, nullable=True)

    password = Column(String, nullable=False)

    role = Column(
        Enum(UserRole, name="user_roles"),
        nullable=False
    )

    membership_id = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )

    # Account is enabled/disabled
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    # Admin approval
    is_approved = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )