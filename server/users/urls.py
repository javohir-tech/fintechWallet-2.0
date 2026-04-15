from django.urls import path

from .views import SignUpView, VerifyCodeView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
]
