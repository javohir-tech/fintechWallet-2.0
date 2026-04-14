from users.models  import User
from .tokens import RegistrationToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthenticationRegistration(JWTAuthentication):
    
    pass