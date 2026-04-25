from django.shortcuts import render
from wallet.models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .services import create_transfer
from decimal import Decimal


class CreateTransactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_wallet = self.request.user.wallet
        to_wallet_id = request.data["wallet_id"]
        amount = request.data["amount"]
        to_wallet = Wallet.objects.filter(id=to_wallet_id).first()
        idempotency_key = request.data["idempotency_key"]

        if to_wallet is None:
            raise ValidationError("user topilmadi")

        result = create_transfer(from_wallet, to_wallet, Decimal(amount), idempotency_key)

        print("=" * 50)
        print(result)
        print("=" * 50)
        
        return Response()
