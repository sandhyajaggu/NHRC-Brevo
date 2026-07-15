import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings
from app.templates.otp_email import otp_email_template


# ============================================================
# BREVO CONFIGURATION
# ============================================================

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = settings.BREVO_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


# ============================================================
# COMMON EMAIL SERVICE
# ============================================================

class BrevoEmailService:

    @staticmethod
    def send_email(
        to_email: str,
        subject: str,
        html_content: str
    ):

        sender = {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        }

        to = [
            {
                "email": to_email
            }
        ]

        email = sib_api_v3_sdk.SendSmtpEmail(
            sender=sender,
            to=to,
            subject=subject,
            html_content=html_content
        )

        try:

            api_instance.send_transac_email(email)

            print(f"Email sent successfully to {to_email}")

            return True

        except ApiException as e:

            print("Brevo Error:", e)

            return False


# ============================================================
# OTP EMAIL
# ============================================================

def send_otp_email(
    email: str,
    otp: str
):

    html = otp_email_template(otp)

    return BrevoEmailService.send_email(
        to_email=email,
        subject="NHRC Email Verification OTP",
        html_content=html
    )


# ============================================================
# RESET PASSWORD EMAIL
# ============================================================

def send_reset_password_email(
    email: str,
    otp: str
):

    html = f"""
    <html>

    <body
        style="
            font-family:Arial;
            padding:20px;
        "
    >

        <h2>
            National Human Resource Club
        </h2>

        <p>Hello,</p>

        <p>
            We received a request to reset your password.
        </p>

        <p>Your OTP is:</p>

        <h1
            style="
                color:#0B6EFD;
                letter-spacing:5px;
            "
        >
            {otp}
        </h1>

        <p>
            This OTP is valid for
            <strong>10 minutes</strong>.
        </p>

        <p>
            If you did not request this,
            simply ignore this email.
        </p>

        <br>

        <p>
            Regards,<br>
            NHRC Team
        </p>

    </body>

    </html>
    """

    return BrevoEmailService.send_email(
        to_email=email,
        subject="NHRC Password Reset OTP",
        html_content=html
    )


# ============================================================
# WELCOME EMAIL
# ============================================================

def send_welcome_email(
    email: str,
    name: str
):

    html = f"""
    <html>

    <body>

        <h2>
            Welcome {name}
        </h2>

        <p>
            Thank you for registering with
            <b>National Human Resource Club</b>.
        </p>

        <p>
            We are delighted to have you with us.
        </p>

    </body>

    </html>
    """

    return BrevoEmailService.send_email(
        to_email=email,
        subject="Welcome to NHRC",
        html_content=html
    )


# ============================================================
# JOB FAIR APPROVED
# ============================================================

def send_job_fair_approved(
    email: str,
    name: str
):

    html = f"""
    <html>

    <body>

        <h2>Hello {name}</h2>

        <p>

            Congratulations!

            <br><br>

            Your Job Fair Registration has been approved.

        </p>

    </body>

    </html>
    """

    return BrevoEmailService.send_email(
        to_email=email,
        subject="Job Fair Registration Approved",
        html_content=html
    )


# ============================================================
# JOB FAIR REJECTED
# ============================================================

def send_job_fair_rejected(
    email: str,
    name: str
):

    html = f"""
    <html>

    <body>

        <h2>Hello {name}</h2>

        <p>

            Unfortunately,

            <br><br>

            Your Job Fair Registration has been rejected.

        </p>

    </body>

    </html>
    """

    return BrevoEmailService.send_email(
        to_email=email,
        subject="Job Fair Registration Rejected",
        html_content=html
    )