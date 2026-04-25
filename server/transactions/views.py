from decimal import Decimal

# ================== DJANGO ===================
from django.shortcuts import render

# ================ MODELS =====================
from wallet.models import Wallet

# ==================== REST FRAMEWORK =======================
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# ============= SERVICES ===================
from .services import create_transfer

# =========== SERIALIZERS ==============
from .serializers import CreateTransactionSerializer, TransactionSerializer


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
