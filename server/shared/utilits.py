# =================== PYTHON ==============
import re
import threading

# =============== MODELS ==============
from users.models import AuthType

# ============== REST FRAMEWORK ===============
from rest_framework.exceptions import ValidationError

# ==================== DJANGO===============
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def check_user_input(email_or_number):
    phone_regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    email_regex = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"

    if re.match(email_regex, email_or_number):
        return AuthType.VIA_EMAIL
    elif re.match(phone_regex, email_or_number):
        return AuthType.VIA_PHONE
    else:
        raise ValidationError("Email or phone number is invalid")


class EmailThread(threading.Thread):
    def __init__(self, email):
        super().__init__()
        self.email = email

    def run(self):
        return self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            to=[data["email_to"]],
        )

        if data["content_type"] == "html":
            email.content_subtype = "html"

        EmailThread(email).start()


def send_email(email: str, code: str):
    html_content = render_to_string(
        "email/verify_code.html", {"code": code, "to_email": email}
    )

    Email.send_email(
        {
            "subject": "Tastiqlsh Kodi",
            "body": html_content,
            "content_type": "html",
            "email_to": email,
        }
    )


def validator_image_size(image):
    max_image_mb = 2

    if image.size > max_image_mb * 1024 * 1024:
        raise ValidationError(f"Image size must be lass than {max_image_mb}")


def check_password(password):
    password_regex = (
        r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    )

    if re.match(password_regex, password):
        raise ValidationError(
            "Password must be at least 8 characters, include uppercase, lowercase, number, and special character."
        )
        
    
