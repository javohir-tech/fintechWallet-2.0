from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

#  =================== MODELS =================
from shared.models import BaseModel
from wallet.models import Wallet


class Transaction(BaseModel):

    class TxType(models.TextChoices):
        TOPUP = "TOPUP", "Hisob To'ldirish"
        TRANSFER = "TRANSFER", "Pul O'tkazish"
        WITHDRAW = "WITHDRAW", "Pul Yechish"

    class TxStatus(models.TextChoices):
        PENDING = "PENDING", "Kutilmoqda"
        SUCCESS = "SUCCESS", "Bajarildi"
        FAILED = "FAILED", "Muvaffaqiyatsiz"
        REVERSED = "REVERSED", "Qaytarildi"

    txtype = models.CharField(max_length=10, choices=TxType.choices)
    status = models.CharField(
        max_length=10, choices=TxStatus.choices, default=TxStatus.PENDING
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )

    fee = models.DecimalField(max_digits=18, decimal_places=2, default=Decimal("0.00"))

    from_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="sent_transactions",
        null=True,
        blank=True,
    )

    to_wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name="received_transactions",
        null=True,
        blank=True,
    )
    
    


# Create your models here.
