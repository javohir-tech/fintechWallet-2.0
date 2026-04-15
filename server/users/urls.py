from django.urls import path

from .views import SignUpView, VerifyCodeView, UpadateVerifyCodeView , UpdateUserView

urlpatterns = [
    path("signup/", SignUpView.as_view()),
    path("verify/", VerifyCodeView.as_view()),
    path("update_verify/", UpadateVerifyCodeView.as_view()),
    path("update/" , UpdateUserView.as_view())
]
