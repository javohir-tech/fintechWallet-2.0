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
            "expiry_year"
        ]
