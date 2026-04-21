from django.urls import path

from .views import WalletMeView

urlpatterns = [
    path("me/", WalletMeView.as_view()),
]
