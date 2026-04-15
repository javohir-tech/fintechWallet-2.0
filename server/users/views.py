# ================ DJANGO =================
from django.utils import timezone
from django.shortcuts import render

# =============== REST FRAMEWORK ==========
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny

# ================ PYTHON ================
from datetime import timedelta

# ==================== SERIALIZER ==================
from .serializers import SignUpSerializer, VerifyCodeSerializer, UpdateUserSerializer

# ================= MODELS ====================
from users.models import User, UserConfirmation, AuthStatus, AuthType

# ================ AUTHENTICATED ================
from .authentication import AuthenticationRegistration

# =============== PERMISSIONS ===================
from .permissions import (
    isRegistrationTokenPermissions,
    CanVerifyCodeSendPermission,
    CanUpdateUserPermission,
)

# =============== TOKENS ======================
from .tokens import RegistrationToken

# =============== SHARED ======================
from shared.utilits import send_email


class SignUpView(generics.CreateAPIView):
    """SIGNUP VIEW"""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer


class VerifyCodeView(APIView):
    authentication_classes = [AuthenticationRegistration]
    permission_classes = [isRegistrationTokenPermissions, CanVerifyCodeSendPermission]

    def post(self, request):

        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code", None)
        user: User = self.request.user

        user_confirmation = UserConfirmation.objects.filter(
            user=user, code=code, expire_time__gt=timezone.now(), is_confirmed=False
        )

        if user_confirmation.exists():
            user.auth_status = AuthStatus.VERIFYED
            user.save()

            user_confirmation.first().is_confirmed = True
            user_confirmation.first().save()

            token = RegistrationToken.for_user(user)

            return Response(
                {
                    "success": True,
                    "message": "successfully is verifited",
                    "data": {
                        "id": str(user.id),
                        "auth_status": user.auth_status,
                        "update_token": str(token),
                    },
                }
            )

        raise ValidationError("code is Invalid or life time has finished")


class UpadateVerifyCodeView(APIView):

    authentication_classes = [AuthenticationRegistration]
    permission_classes = [isRegistrationTokenPermissions]

    def post(self, request):

        user: User = self.request.user

        if UserConfirmation.objects.filter(
            expire_time__gt=timezone.now(), user=user, is_confirmed=False
        ).exists():
            raise ValidationError("you are have valid token . please wait life time")

        try:
            if user.auth_type == AuthType.VIA_EMAIL:
                email = user.email
                code = user.create_code(AuthType.VIA_EMAIL)
                send_email(email, code)
            elif user.auth_status == AuthType.VIA_PHONE:
                phone_number = user.phone_number
                code = user.create_code(AuthType.VIA_PHONE)
                send_email(phone_number, code)
        except Exception as e:
            raise ValidationError(f"nimadir error {e}")

        return Response(
            {"success": True, "message": "we are send verify code your address"}
        )


class UpdateUserView(generics.UpdateAPIView):
    authentication_classes = [AuthenticationRegistration]
    permission_classes = [isRegistrationTokenPermissions, CanUpdateUserPermission]
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user
