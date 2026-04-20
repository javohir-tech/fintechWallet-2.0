# ================ DJANGO ====================
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator

# ================ MODELS ====================
from shared.models import BaseModel
from users.models import User


class Wallet(BaseModel):

    class Currency(models.TextChoices):
        UZS = "UZS", "O'zbek So'mi"
        USD = "USD", "AQSH Dolleri"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wallet")

    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(
                Decimal("0.00"),
            )
        ],
    )

    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.UZS
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "wallets"

    def __str__(self):
        return f"{self.user}-{self.balance} {self.currency}"

    def has_enough_balance(self, amount: Decimal) -> bool:
        return self.balance >= amount

    def debit(self, amount: Decimal):

        if not self.has_enough_balance(amount):
            raise ValueError("Balans  yetarli emas")
        self.balance -= amount
        self.save(update_fields=["balance", "updated_time"])

    def credit(self, amount: Decimal):
        self.balance += amount
        self.save(update_fields=["balance", "updated_time"])

