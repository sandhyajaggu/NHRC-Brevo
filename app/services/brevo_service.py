import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings
from app.templates.otp_email import otp_email_template


class BrevoEmailService:

    def __init__(self):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key["api-key"] = settings.BREVO_API_KEY

        self.api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
    ):

        smtp_email = sib_api_v3_sdk.SendSmtpEmail(

            sender={
                "name": settings.BREVO_SENDER_NAME,
                "email": settings.BREVO_SENDER_EMAIL,
            },

            to=[
                {
                    "email": to_email
                }
            ],

            subject=subject,

            html_content=html_content,
        )

        try:

            response = self.api_instance.send_transac_email(
                smtp_email
            )

            return {
                "success": True,
                "message": "Email sent successfully",
                "message_id": response.message_id,
            }

        except ApiException as e:

            print("Brevo Error:", e)

            return {
                "success": False,
                "message": str(e),
            }


brevo_service = BrevoEmailService()


# ============================================================
# OTP EMAIL
# ============================================================

def send_otp_email(email: str, otp: str):

    html = otp_email_template(otp)

    return brevo_service.send_email(

        to_email=email,

        subject="NHRC Email Verification OTP",

        html_content=html,
    )


# ============================================================
# RESET PASSWORD
# ============================================================

def send_reset_password(email: str, otp: str):

    html = otp_email_template(otp)

    return brevo_service.send_email(

        to_email=email,

        subject="NHRC Password Reset OTP",

        html_content=html,
    )


# ============================================================
# WELCOME EMAIL
# ============================================================

def send_welcome_email(email: str, name: str):

    html = f"""
    <html>
    <body>

        <h2>Welcome {name}</h2>

        <p>
            Thank you for registering with
            <b>National Human Resource Club</b>.
        </p>

    </body>
    </html>
    """

    return brevo_service.send_email(

        to_email=email,

        subject="Welcome to NHRC",

        html_content=html,
    )


# ============================================================
# JOB FAIR APPROVED
# ============================================================

def send_job_fair_approved(email: str, name: str):

    html = f"""
    <html>
    <body>

        <h2>Hello {name}</h2>

        <p>
            Congratulations!

            Your Job Fair Registration has been approved.
        </p>

    </body>
    </html>
    """

    return brevo_service.send_email(

        to_email=email,

        subject="Job Fair Registration Approved",

        html_content=html,
    )


# ============================================================
# JOB FAIR REJECTED
# ============================================================

def send_job_fair_rejected(email: str, name: str):

    html = f"""
    <html>
    <body>

        <h2>Hello {name}</h2>

        <p>
            Unfortunately your Job Fair Registration
            has been rejected.
        </p>

    </body>
    </html>
    """

    return brevo_service.send_email(

        to_email=email,

        subject="Job Fair Registration Rejected",

        html_content=html,
    )