import uuid
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

    # ── Idempotency — ikki marta yechmaslik ─
    idempotency_key = models.CharField(
        max_length=64, unique=True, null=True, blank=True, db_index=True
    )

    debit_amount = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True
    )

    credit_amount = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True
    )

    reference = models.CharField(max_length=64, unique=True, default=uuid.uuid4)

    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_time"]
        indexes = [
            models.Index(fields=["from_wallet", "-created_time"]),
            models.Index(fields=["to_wallet", "-created_time"]),
            models.Index(fields=["status"]),
            models.Index(fields=["idempotency_key"]),
        ]

    def __str__(self):
        return f"{self.txtype} | {self.amount} | {self.status}"

    @property
    def is_balanced(self):
        if self.debit_amount and self.credit_amount:
            return self.debit_amount + self.credit_amount == 0
        return True


# Create your models here.
