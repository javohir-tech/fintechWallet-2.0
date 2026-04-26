from rest_framework import serializers
from wallet.models import Wallet
from .models import Transaction
from decimal import Decimal

from cards.serializers import CardTransactionSerializer


class CreateTransactionSerializer(serializers.Serializer):
    wallet_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    idempotency_key = serializers.CharField(max_length=64)

    def validate_wallet_id(self, value):
        if not Wallet.objects.filter(id=value).exists():
            raise serializers.ValidationError("Wallet topilmadi")

        return value

    def validate(self, attrs):
        request = self.context.get("request")

        if request and hasattr(request.user, "wallet"):
            me_wallet_id = request.user.wallet.id
            if me_wallet_id == attrs["wallet_id"]:
                raise serializers.ValidationError(
                    "ozingizga transaksiya qila olmaysiz "
                )

        return attrs


class TransactionSerializer(serializers.ModelSerializer):

    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "status",
            "txtype",
            "fee",
            "idempotency_key",
            "description",
            "metadata",
            "debit_amount",
            "credit_amount",
            "from_user",
            "to_user",
        ]

    def get_from_user(self, obj):
        from_card = obj.from_wallet.cards.filter(wallet=obj.from_wallet).first()
        if not from_card is None:
            return CardTransactionSerializer(from_card).data
        return None

    def get_to_user(self, obj):
        to_card = obj.to_wallet.cards.filter(wallet=obj.to_wallet).first()
        if not to_card is None:
            return CardTransactionSerializer(to_card).data
        return None


class AllTransactionsSerializer(serializers.ModelSerializer):
    from_user = serializers.SerializerMethodField()
    to_user = serializers.SerializerMethodField()
    direction = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "amount",
            "status",
            "txtype",
            "fee",
            "idempotency_key",
            "description",
            "metadata",
            "debit_amount",
            "credit_amount",
            "from_user",
            "to_user",
            "direction"
        ]

    def get_from_user(self, obj):
        from_card = obj.from_wallet.cards.all().first()
        if not from_card is None:
            return CardTransactionSerializer(from_card).data
        return None

    def get_to_user(self, obj):
        to_card = obj.to_wallet.cards.all().first()
        if not to_card is None:
            return CardTransactionSerializer(to_card).data
        return None

    def get_direction(self, obj):
        request = self.context.get("request")

        if request and hasattr(request, "user"):
            user = request.user
            if user:
                return user.id == obj.to_wallet.user.id
            return None
        return None