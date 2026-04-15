from users.models import User
from .tokens import RegistrationToken
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class AuthenticationRegistration(JWTAuthentication):

    def get_validated_token(self, raw_token):
        try:
            return RegistrationToken(raw_token)
        except Exception as e:
            raise AuthenticationFailed(f"token xatosi : {e}")

    def get_user(self, validated_token):
        try:
            user_id = validated_token.get("user_id", None)

            if user_id is None:
                raise AuthenticationFailed("token ichida user_id yo'q")

            user: User = User.objects.get(id=user_id)

            if user.auth_status != validated_token.get("auth_stutus", None):
                raise AuthenticationFailed("Token yaroqsiz")

            return user
        except User.DoesNotExist:
            raise AuthenticationFailed("user topilmadi")
        except Exception as e:
            raise AuthenticationFailed(f"Token hatosi {e}")
