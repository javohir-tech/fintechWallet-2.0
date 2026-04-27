from decimal import Decimal

# ================== DJANGO ===================
from django.shortcuts import render
from django.db.models import Q, Prefetch

# ================ MODELS =====================
from wallet.models import Wallet
from .models import Transaction
from cards.models import Card

# ==================== REST FRAMEWORK =======================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
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
        user   = self.request.user
        wallet = user.wallet
        params = self.request.query_params

        qs = Transaction.objects.filter(
            Q(from_wallet=wallet) | Q(to_wallet=wallet)
        )

        # ?status=SUCCESS,PENDING
        status = params.get("status")
        if status:
            qs = qs.filter(status__in=status.upper().split(","))

        # ?txtype=TRANSFER
        txtype = params.get("txtype")
        if txtype:
            qs = qs.filter(txtype__in=txtype.upper().split(","))

        # ?direction=in  →  faqat kiruvchi
        # ?direction=out →  faqat chiquvchi
        direction = params.get("direction")
        if direction == "in":
            qs = qs.filter(to_wallet=wallet)
        elif direction == "out":
            qs = qs.filter(from_wallet=wallet)

        return qs


class TransactionDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AllTransactionsSerializer
    queryset = Transaction.objects.all()

    def get_object(self):
        pk = self.kwargs["pk"]
        user = self.request.user

        transaction = (
            Transaction.objects.select_related(
                "from_wallet",
                "from_wallet__user",
                "to_wallet",
                "to_wallet__user",
            )
            .prefetch_related(
                Prefetch(
                    "from_wallet__cards", queryset=Card.objects.filter(is_active=True)
                ),
                Prefetch(
                    "to_wallet__cards", queryset=Card.objects.filter(is_active=True)
                ),
            )
            .filter(id=pk)
            .first()
        )

        if transaction is None:
            raise ValidationError("transaksiya topilmadi")

        if (
            transaction.from_wallet.user.id != user.id
            and transaction.to_wallet.user.id != user.id
        ):
            raise PermissionDenied("Bu transaksiyani ko'rish huquqingiz yo'q")

        return transaction
