from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.event_registration import EventRegistration
from app.models.job_fair import JobFair
from app.models.training_registration import TrainingRegistration
from app.schemas.jobfair import JobFairCreate, JobFairResponse, JobFairUpdate
from app.schemas.registration import RegistrationCreate
from app.schemas.training_registration_create import TrainingRegistrationCreate
from app.models.training_program import TrainingProgram
router = APIRouter(
    prefix="/registration",
    tags=["Registration"]
)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User, UserRole
from app.core.security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    payload: RegistrationCreate,
    db: Session = Depends(get_db)
):

    # ==========================================
    # CHECK EMAIL
    # ==========================================

    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # ==========================================
    # CHECK MOBILE
    # ==========================================

    if payload.mobile:

        existing_mobile = (
            db.query(User)
            .filter(User.mobile == payload.mobile)
            .first()
        )

        if existing_mobile:
            raise HTTPException(
                status_code=400,
                detail="Mobile number already registered"
            )

    # ==========================================
    # PASSWORD VALIDATION
    # ==========================================

    if payload.password != payload.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # ==========================================
    # ROLE VALIDATION
    # ==========================================

    try:
        role = UserRole(payload.role.lower())
    except ValueError:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid role. Allowed roles: "
                "employee, student, representative, "
                "member, tpo"
            )
        )

    # ==========================================
    # CREATE USER
    # ==========================================

    user = User(

        full_name=payload.full_name,

        email=payload.email,

        mobile=payload.mobile,

        password=hash_password(payload.password),

        role=role,

        membership_id=payload.membership_id,

        # VERY IMPORTANT
        is_active=True,

        # VERY IMPORTANT
        is_approved=False
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    # ==========================================
    # RESPONSE
    # ==========================================

    return {

        "message": (
            "Registration successful. "
            "Your account is waiting for admin approval."
        ),

        "user_id": user.id,

        "nhrc_id": user.membership_id,

        "full_name": user.full_name,

        "email": user.email,

        "role": user.role.value,

        "is_approved": user.is_approved,

        "is_active": user.is_active
    }
@router.post("/training/register")
def register_training(

    payload: TrainingRegistrationCreate,

    db: Session = Depends(get_db),

    current_user=Depends(get_current_user)

):

    role = current_user.role.strip().upper()

    # Only Student and Employee

    if role not in ["STUDENT", "EMPLOYEE"]:

        raise HTTPException(
            status_code=403,
            detail="Only Student and HR can register"
        )

    training = db.query(
        TrainingProgram
    ).filter(
        TrainingProgram.id == payload.training_id
    ).first()

    if not training:

        raise HTTPException(
            status_code=404,
            detail="Training Program not found"
        )

    # Prevent Duplicate Registration

    existing = db.query(
        TrainingRegistration
    ).filter(
        TrainingRegistration.training_id == payload.training_id,
        TrainingRegistration.member_id == current_user.id
    ).first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Already Registered"
        )

    # Student Validation

    if role == "STUDENT":

        if not payload.college_name:
            raise HTTPException(
                status_code=400,
                detail="college_name required"
            )

        if not payload.year_of_passout:
            raise HTTPException(
                status_code=400,
                detail="year_of_passout required"
            )

    # HR Validation

    if role == "EMPLOYEE":

        if not payload.company_name:
            raise HTTPException(
                status_code=400,
                detail="company_name required"
            )

        if not payload.company_location:
            raise HTTPException(
                status_code=400,
                detail="company_location required"
            )

    registration = TrainingRegistration(

        training_id=payload.training_id,

        member_id=current_user.id,

        member_type="HR" if role == "EMPLOYEE" else "STUDENT",

        full_name=payload.full_name,

        email=current_user.email,

        phone=payload.phone,

        location=payload.location,

        iam_a=payload.iam_a,

        nhrc_id=payload.nhrc_id,

        receive_updates=payload.receive_updates,

        college_name=payload.college_name,

        year_of_passout=payload.year_of_passout,

        company_name=payload.company_name,

        company_location=payload.company_location,

        status="REGISTERED",

        created_at=datetime.utcnow()
    )

    db.add(registration)

    db.commit()

    db.refresh(registration)

    return {
        "message": "Training Registration Successful",
        "registration_id": registration.id
    }

