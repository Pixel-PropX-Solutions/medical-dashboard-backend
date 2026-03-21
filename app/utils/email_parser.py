"""------------------------------------------------------------------------------------------------------------------------
                                                    TEMPLATE MODULE
------------------------------------------------------------------------------------------------------------------------
"""

from datetime import datetime, timezone
from app.config import settings


class Template:
    """
    TEMPLATE MODULE
    ---------------
    Parser for Dynamic html Render & Storage
    """

    # --------------------------------------------------------------------------------------------------------------------------

    def __init__(self, domain, env):
        # Initialise html paths
        self.directory = "app/utils/templates/"
        self.domain = domain
        self.domain_login = domain + "/login"
        self.onboard_html = self.directory + "onboard.html"
        self.password_reset_html = self.directory + "password_reset.html"
        self.query_message_html = self.directory + "query_message.html"
        
    # --------------------------------------------------------------------------------------------------------------------------

    def render_template(self, path, parser):
        """
        RENDER_TEMPLATE
        ---------------
        Renders the html file from *path* by replacing *parser* arguments,
        and returns the rendered string.
        ...
        """

        # Open html file
        with open(path, "r", encoding="utf8") as html:
            content = html.read()
            for key in parser:
                content = content.replace(
                    "{" + key + "}",
                    str(parser[key]),
                )
            return content

    # --------------------------------------------------------------------------------------------------------------------------

    def Onboard(self, email, password, name):
        parser = {
            "password": password,
            "name": name,
            "email": email,
            "domain": self.domain,
            "domain_login": self.domain_login,
        }
        return self.render_template(self.onboard_html, parser)

    def NewPasswordRequest(self, name, email, password):
        """PASSWORD REQUEST EMAIL
        --------------------
        Generates a password request email template with the provided details.
        Parameters:
        - name: Name of the user.
        - email: Email address of the user.
        - password: New Random Password for the user.
        Returns:
        - Rendered HTML string for the password request email.
        """

        parser = {
            "link": self.domain_login,
            "name": name,
            "email": email,
            "password": password,
        }
        return self.render_template(self.password_reset_html, parser)

    def QueryEmail(self, fullName, email, phone, message, messageType):
        """QUERY_EMAIL
        --------------------
        Generates a query email template with the provided details.
        Parameters:
        - fullName: Name of the user.
        - email: Email address of the user.
        - phone: Phone number of the user.
        - message: Message from the user.
        - messageType: Type of message.
        Returns: 
        - Rendered HTML string for the query email.
        """

        parser = {
            "full_name": fullName,
            "email": email,
            "phone_number": phone,
            "message": message,
            "message_type": messageType,
            "timestamp": str(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")),
        }
        return self.render_template(self.query_message_html, parser)
