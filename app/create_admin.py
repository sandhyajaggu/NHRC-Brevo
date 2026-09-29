import os
import sys

from dotenv import load_dotenv
from sqlalchemy import func

from app.core.database import SessionLocal

from app.models.member import Member

from app.core.security import hash_password


load_dotenv()


def create_admin():

    # Credentials come from the environment so they never live in the repo.
    email = (os.getenv("ADMIN_EMAIL") or "").strip().lower()
    password = (os.getenv("ADMIN_PASSWORD") or "").strip()
    full_name = os.getenv("ADMIN_NAME", "Administrator")

    if not email or not password:
        sys.exit("Set ADMIN_EMAIL and ADMIN_PASSWORD before running this script")

    db = SessionLocal()

    existing = db.query(Member).filter(
        func.lower(Member.email) == email
    ).first()

    if existing:

        # Re-running the script resets the admin password, role and status
        existing.role = "ADMIN"

        existing.status = "approved"

        existing.password_hash = hash_password(password)

        db.commit()

        print("Admin already exists - role and password updated")

        return

    admin = Member(

        membership_id="ADMIN001",

        full_name=full_name,

        email=email,

        password_hash=hash_password(password),

        role="ADMIN",

        candidate_type="admin",

        status="approved"
    )

    db.add(admin)

    db.commit()

    print("Admin created successfully")


if __name__ == "__main__":
    create_admin()
