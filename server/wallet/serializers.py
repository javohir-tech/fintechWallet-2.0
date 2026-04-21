from rest_framework import serializers
from .models import Wallet


class WalletMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ["id", "balance", "currency", "is_active"]
