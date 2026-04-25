from django.urls import path
from .views import CreateTransactionView, GetAllTransactionsView, TransactionDetailView

urlpatterns = [
    path("create-transfer/", CreateTransactionView.as_view()),
    path("transactions/", GetAllTransactionsView.as_view()),
    path("transactions/<uuid:pk>/" , TransactionDetailView.as_view())
]
