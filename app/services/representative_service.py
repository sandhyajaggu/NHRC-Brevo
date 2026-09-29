from fastapi import HTTPException
from app.models.member import Member
from app.repositories.representative_repository import RepresentativeRepository
from app.utils.registration_response import registration_response


class RepresentativeService:

    @staticmethod
    def _get_member_id(db, membership_id: str):
        member = db.query(Member).filter_by(
            membership_id=membership_id
        ).first()

        if not member:
            print(" MEMBER NOT FOUND:", membership_id)
            raise HTTPException(status_code=404, detail="Member not found")

        return member.id


    @staticmethod
    def _prepare_data(payload, member_id):
        data = payload.dict()
        data["member_id"] = member_id
        data.pop("membership_id", None)
        return data


    @staticmethod
    def _build_response(db, obj):
        member = db.query(Member).filter_by(id=obj.member_id).first()

        return registration_response(member, obj)


    # 🔹 UNIVERSITY
    @staticmethod
    def create_university(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_university(db, data)

        return RepresentativeService._build_response(db, obj)


    # 🔹 AUTONOMOUS
    @staticmethod
    def create_autonomous(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_autonomous(db, data)

        return RepresentativeService._build_response(db, obj)


    # 🔹 BOTH
    @staticmethod
    def create_both(db, payload):
        member_id = RepresentativeService._get_member_id(db, payload.membership_id)
        data = RepresentativeService._prepare_data(payload, member_id)

        obj = RepresentativeRepository.create_both(db, data)

        return RepresentativeService._build_response(db, obj)
    