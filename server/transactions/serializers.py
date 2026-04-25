from rest_framework import serializers
from wallet.models import Wallet
from decimal import Decimal


class CreateTransactionSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=64)

    def validate_wallet_id(self, value):
        if not Wallet.objects.filter(id=value).exists():
            raise serializers.ValidationError("Wallet topilmadi")

    def validate(self, attrs):
        request = self.context.get("request")

        if request and hasattr(request.user, "wallet"):
            me_wallet_id = request.user.wallet.id
            if me_wallet_id == attrs["wallet_id"]:
                raise serializers.ValidationError(
                    "ozingizga transaksiya qila olmaysiz "
                )
