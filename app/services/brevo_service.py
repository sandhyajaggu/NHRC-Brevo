import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from app.core.config import settings


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

        sender = {
            "name": settings.BREVO_SENDER_NAME,
            "email": settings.BREVO_SENDER_EMAIL
        }

        receiver = [
            {
                "email": to_email
            }
        ]

        email = sib_api_v3_sdk.SendSmtpEmail(

            sender=sender,

            to=receiver,

            subject=subject,

            html_content=html_content

        )

        try:

            response = self.api_instance.send_transac_email(email)

            return {
                "success": True,
                "message_id": response.message_id
            }

        except ApiException as e:

            return {
                "success": False,
                "error": str(e)
            }


brevo_service = BrevoEmailService()