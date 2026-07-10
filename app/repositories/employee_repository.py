from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.models.member import Member
from app.models.employee import Employee


class EmployeeRepository:

    @staticmethod
    def create(db: Session, payload: dict):
        employee = Employee(**payload)

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee

    @staticmethod
    def get_by_email(db: Session, email: str):

        return (
            db.query(Employee)
            .filter(Employee.official_email == email)
            .first()
        )

    @staticmethod
    def get_employees_with_details(db: Session):

        results = (
            db.query(Member, Employee)
            .join(Employee, Employee.member_id == Member.id)
            .filter(Member.candidate_type == "employee")
            .all()
        )

        return jsonable_encoder([
            {
                "member": member,
                "details": employee
            }
            for member, employee in results
        ])