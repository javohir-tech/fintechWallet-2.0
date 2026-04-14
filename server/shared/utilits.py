import re
from users.models import AuthType
from rest_framework.exceptions import ValidationError


def check_user_input(email_or_number):
    phone_regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    email_regex = r"[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+"

    if re.match(email_regex, email_or_number):
        return AuthType.VIA_EMAIL
    elif re.match(phone_regex, email_or_number):
        return AuthType.VIA_PHONE
    else:
        return None
