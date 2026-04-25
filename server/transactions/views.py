from decimal import Decimal

# ================== DJANGO ===================
from django.shortcuts import render
from django.db.models import Q

# ================ MODELS =====================
from wallet.models import Wallet
from .models import Transaction

# ==================== REST FRAMEWORK =======================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import generics

# ============= SERVICES ===================
from .services import create_transfer

# =========== SERIALIZERS ==============
from .serializers import (
    CreateTransactionSerializer,
    TransactionSerializer,
    AllTransactionsSerializer,
)


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        seriallizer = CreateTransactionSerializer(
            data=request.data, context={"request": request}
        )
        seriallizer.is_valid(raise_exception=True)

        data = seriallizer.validated_data
        from_wallet = self.request.user.wallet
        to_wallet = Wallet.objects.get(id=data["wallet_id"])

        amount = data["amount"]
        idempotency_key = data["idempotency_key"]

        if to_wallet is None:
            raise ValidationError("user topilmadi")

        transaction = create_transfer(from_wallet, to_wallet, amount, idempotency_key)

        transaction_serializer = TransactionSerializer(transaction)

        return Response(transaction_serializer.data)


class GetAllTransactionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AllTransactionsSerializer

    def get_queryset(self):
        user = self.request.user
        wallet_id = user.wallet
        return Transaction.objects.filter(
            Q(from_wallet=wallet_id) | Q(to_wallet=wallet_id)
        )
        
class TransactionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AllTransactionsSerializer
    queryset =  Transaction.objects.all()   
