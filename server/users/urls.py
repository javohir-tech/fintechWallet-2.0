from django.urls import path

from .views import (
    SignUpView,
    VerifyCodeView,
    UpadateVerifyCodeView,
    UpdateUserView,
    UploadAvatarView,
    LogOutView, 
    LoginView,
    ForgetPasswordView,
    UpdatePasswordView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("update_verify/", UpadateVerifyCodeView.as_view()),
    path("update/", UpdateUserView.as_view()),
    path("avatar/", UploadAvatarView.as_view()),
    path("logout/", LogOutView.as_view()),
    path("login/", LoginView.as_view()),
    path("forget/", ForgetPasswordView.as_view()),
    path("password/", UpdatePasswordView.as_view()),
]
