from django.urls import path

from .views import WalletMeView, WalletMeHistoryView

urlpatterns = [
    path("me/", WalletMeView.as_view()),
    path("me/balance-history/", WalletMeHistoryView.as_view()),
]
