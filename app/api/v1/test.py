from fastapi import APIRouter

from app.services.brevo_service import BrevoEmailService

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

@router.get("/brevo")
def test_brevo():

    service = BrevoEmailService()

    success = service.send_email(
        to_email="suryatejaperiketi570@gmail.com",
        subject="NHRC OTP Test",
        html_content="""
        <h2>National Human Resource Club</h2>

        <h3>Your OTP is:</h3>

        <h1>123456</h1>

        
        """
    )

    return {
        "success": success
    }