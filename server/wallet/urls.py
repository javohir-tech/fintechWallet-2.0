from django.urls import path
from .views import WalletMeView, WalletStatsView

urlpatterns = [
    path("me/", WalletMeView.as_view()),
    path("stats/", WalletStatsView.as_view()),
]
