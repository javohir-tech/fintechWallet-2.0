from users.models import User
from datetime import timedelta
from rest_framework_simplejwt.tokens import Token


class RegistrationToken(Token):

    token_type = "registration"
    lifetime = timedelta(minutes=15)

    @classmethod
    def for_user(cls, user: User):
        token = cls()

        token["user_id"] = user.id
        token["auth_stutus"] = user.auth_status
        token["token_type"] = "registration"
        token["auth_type"] = user.auth_type

        return token

    @classmethod
    def get_user_from_token(cls, str_token):
        try:
            token = cls(str_token)

            user_id = token.get("user_id")

            user = User.objects.filter(id=user_id)

            return user
        except Exception:
            return None
