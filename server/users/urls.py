from django.urls import path

from .views import (
    SignUpView,
    VerifyCodeView,
    UpadateVerifyCodeView,
    UpdateUserView,
    UploadAvatarView,
    LogOutView,
)

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("update_verify/", UpadateVerifyCodeView.as_view()),
    path("update/", UpdateUserView.as_view()),
    path("avatar/", UploadAvatarView.as_view()),
    path("logout/", LogOutView.as_view()),
]
