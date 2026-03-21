"""------------------------------------------------------------------------------------------------------------------------
                                                  EMAILER MODULE
------------------------------------------------------------------------------------------------------------------------
"""

import smtplib
import ssl

# Email Dependencies
from email.message import EmailMessage

# Environment Variables Dependencies
from app.config import settings
from app.utils.email_parser import Template


class Emailer:
    """
    Email Sever on SMTP with Secure SSL
    """

    # ------------------------------------------------------------------------------------------------------------

    def __init__(
        self,
    ) -> None:
        # Initialise Email Server Credentials
        self.SMTP_USERNAME = settings.SMTP_USERNAME
        self.SMTP_PASSWORD = settings.SMTP_PASSWORD
        self.SMTP_SERVER = settings.SMTP_SERVER
        self.SMTP_PORT = settings.SMTP_PORT

    # ------------------------------------------------------------------------------------------------------------

    def send(
        self,
        subject,
        email,
        content,
    ) -> None:
        """
        Sends Email to Clients.

        """
        try:

            msg = EmailMessage()

            # Email Constructor
            msg["From"] = "Clinova <{email}>".format(email=self.SMTP_USERNAME)
            msg["To"] = email
            msg["Subject"] = subject
            msg.add_alternative(
                content,
                subtype="html",
            )

            # Send Mail
            server = smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT)
            server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print(f"Successfully sent email to {email}")
        except Exception as e:
            print(f"Failed to send email to {email}: {e}")
       


template = Template(settings.FRONTEND_DOMAIN, settings.ENVIRONMENT)
mail = Emailer()
