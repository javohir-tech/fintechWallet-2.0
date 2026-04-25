from django.db import models
from datetime import date
from wallet.models import Wallet
from shared.models import BaseModel
from random import randint


class Card(BaseModel):

    class CARD_TYPE(models.TextChoices):
        VIRTUAL = "virtual", "Virtual karta"
        PHYSICAL = "physical", "Physical"

    card_number = models.CharField(max_length=16, unique=True)
    card_holder_name = models.CharField(max_length=100)

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="cards")

    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()

    card_type = models.CharField(
        max_length=8, choices=CARD_TYPE.choices, default=CARD_TYPE.VIRTUAL
    )

    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "cards"
        constraints = [
            models.UniqueConstraint(
                fields=["wallet"],
                condition=models.Q(is_active=True),
                name="unique_active_card_per_wallet",
            )
        ]

    def __str__(self):
        return f"{self.masked_number} and {self.wallet.user}"

    @property
    def masked_number(self):
        n = self.card_number
        return f"**** **** **** {n[-4:]}"

    @staticmethod
    def generate_card_number() -> str:
        prefix = "8600"
        remaning = "".join([str(randint(0, 9)) for _ in range(11)])
        partial = prefix + remaning
        check_digit = Card._luhn_check_digit(partial)
        return partial + str(check_digit)

    @staticmethod
    def _luhn_check_digit(card_number: str) -> int:
        digits = [int(d) for d in card_number]
        digits.reverse()

        total = 0
        for i, digit in enumerate(digits):
            if i % 2 == 0:
                doupled = digit * 2
                total += doupled - 9 if doupled > 9 else doupled
            else:
                total += digit
        return (10 - (total % 10)) % 10

    @classmethod
    def create_for_wallet(cls, wallet, holder_name: str, expiry_year: int = 4):

        if cls.objects.filter(wallet=wallet, is_active=True).exists():
            raise ValueError("har bir user uchun faqat bitta card ochishga ruxsat")

        today = date.today()

        while True:
            number = cls.generate_card_number()
            if not cls.objects.filter(card_number=number).exists():
                break

        cls.objects.create(
            card_number=number,
            wallet=wallet,
            card_holder_name=holder_name,
            expiry_year=today.year + expiry_year,
            expiry_month=today.month,
        )
