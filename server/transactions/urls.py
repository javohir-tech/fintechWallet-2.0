from django.urls import path
from .views import CreateTransactionView

urlpatterns = [
    path("create-transfer/" , CreateTransactionView.as_view())
]
