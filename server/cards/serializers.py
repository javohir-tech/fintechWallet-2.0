from rest_framework import serializers
from .models import Card


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = [
            "card_number",
            "card_holder_name",
            "card_type",
            "expiry_month",
            "expiry_year",
        ]


class CardLookupSerializer(serializers.Serializer):

    card_number = serializers.CharField(max_length=16)

    def validate_card_number(self, value):
        try:
            card = Card.objects.select_related("wallet__user").get(
                card_number=value, is_active=True
            )
        except Card.DoesNotExist:
            raise serializers.ValidationError("karta topilmadi")

        self.card_instance = card
        return value

    def get_result(self):
        user = self.card_instance.wallet.user
        return {
            "masked_number": self.card_instance.masked_number,
            "wallet_id": self.card_instance.wallet.id,
            "username": user.username,
        }


class CardTransactionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Card
        fields = ["username", "masked_number"]

    def get_username(self, obj):
        return obj.wallet.user.username
