from rest_framework import serializers
from .models import Wallet
from cards.serializers import CardSerializer


class WalletMeSerializer(serializers.ModelSerializer):

    card = serializers.SerializerMethodField()
    
    class Meta:
        model = Wallet
        fields = ["id", "balance", "currency", "is_active", "updated_time" ,"card"]
        
        
    def get_card(self ,  obj):
        card = obj.cards.filter(is_active = True).first()
        
        if card :
            return CardSerializer(card).data
        return None
        
    
