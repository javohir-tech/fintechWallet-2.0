# ==================== DJANGO ======================
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum, Q
from django.db.models.functions import (
    TruncDay, TruncWeek, TruncMonth, TruncYear,
)

# ==================== REST FRAMEWORK ==============
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# =================== MODELS ====================
from .models import Wallet
from users.models import User
from transactions.models import Transaction

# ================== Serializers =================
from .serializers import WalletMeSerializer
from cards.serializers import CardSerializer

import datetime


class WalletMeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user: User = self.request.user
        wallet = user.wallet
        serializer = WalletMeSerializer(wallet)
        return Response(serializer.data)


class WalletStatsView(APIView):
    """
    Wallet ga kirgan (income) va chiqqan (outcome) pullar statistikasi.
    ?period=daily | weekly | monthly | yearly
    """
    permission_classes = [IsAuthenticated]

    PERIODS = {
        "daily":   (TruncDay,   7,  "day"),
        "weekly":  (TruncWeek,  8,  "week"),
        "monthly": (TruncMonth, 12, "month"),
        "yearly":  (TruncYear,  5,  "year"),
    }

    def get(self, request):
        period = request.query_params.get("period", "monthly")
        if period not in self.PERIODS:
            period = "monthly"

        trunc_fn, count, unit = self.PERIODS[period]
        wallet = request.user.wallet
        now = timezone.now()

        # Boshlanish sanasini hisoblash
        if unit == "day":
            start = now - datetime.timedelta(days=count - 1)
        elif unit == "week":
            start = now - datetime.timedelta(weeks=count - 1)
        elif unit == "month":
            start = (now.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
            for _ in range(count - 2):
                start = (start - datetime.timedelta(days=1)).replace(day=1)
        else:  # year
            start = now.replace(month=1, day=1) - datetime.timedelta(days=365 * (count - 1))

        # Income: bu walletga pul kelgan tranzaksiyalar
        income_qs = (
            Transaction.objects
            .filter(to_wallet=wallet, status="SUCCESS", created_time__gte=start)
            .annotate(period=trunc_fn("created_time"))
            .values("period")
            .annotate(total=Sum("amount"))
            .order_by("period")
        )

        # Outcome: bu walletdan pul chiqqan tranzaksiyalar
        outcome_qs = (
            Transaction.objects
            .filter(from_wallet=wallet, status="SUCCESS", created_time__gte=start)
            .annotate(period=trunc_fn("created_time"))
            .values("period")
            .annotate(total=Sum("amount"))
            .order_by("period")
        )

        income_map  = {str(r["period"].date()): float(r["total"]) for r in income_qs}
        outcome_map = {str(r["period"].date()): float(r["total"]) for r in outcome_qs}

        # Barcha labellarni to'ldirish
        labels = sorted(set(list(income_map.keys()) + list(outcome_map.keys())))

        data = [
            {
                "label": label,
                "income":  income_map.get(label, 0),
                "outcome": outcome_map.get(label, 0),
            }
            for label in labels
        ]

        return Response({
            "period": period,
            "data": data,
        })

