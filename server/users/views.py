# ================ DJANGO =================
from django.shortcuts import render

# =============== REST FRAMEWORK ==========
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

# ================ PYTHON ================
from datetime import timedelta

# ==================== SERIALIZER ==================
from .serializers import SignUpSerializer

# ================= MODELS ====================
from users.models import User

class SignUpView(generics.CreateAPIView):
    """SIGNUP VIEW"""
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
