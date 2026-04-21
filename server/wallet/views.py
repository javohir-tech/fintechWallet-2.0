# ==================== DJANGO ======================
from django.shortcuts import render

# ==================== REST FRAMEWORK ==============
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# =================== MODELS ====================
from .models import Wallet
from users.models import User

# ================== Serializers =================
from .serializers import WalletMeSerializer


class WalletMeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        user: User = self.request.user
        wallet = user.wallet
        serializer = WalletMeSerializer(wallet)

        return Response(serializer.data)


# Create your views here.
