from rest_framework.permissions import BasePermission
from users.models import AuthStatus


class isRegistrationTokenPermissions(BasePermission):

    def has_permission(self, request, view):

        if not hasattr(request, "auth") and request.auth is None:
            return False

        token_type = request.auth.get("token_type", None)

        return token_type == "registration"


class CanVerifyCodeSendPermission(BasePermission):

    def has_permission(self, request, view):

        if not hasattr(request, "auth") or request.auth is None:
            return False

        auth_status = request.auth.get("auth_status", None)

        return auth_status in [AuthStatus.NEW, AuthStatus.DONE, AuthStatus.LOGOUT , AuthStatus.VERIFYED]


class CanUpdateUserPermission(BasePermission):

    def has_permission(self, request, view):

        if not hasattr(request, "auth") or request.auth is None:
            return False

        auth_status = request.auth.get("auth_status", None)

        return auth_status == AuthStatus.VERIFYED
