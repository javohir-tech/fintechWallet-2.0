from django.db import models
from wallet.models import Wallet
from datetime import date
from shared.models import BaseModel
from random import randint


class Card(BaseModel):

    class CARD_TYPE(models.TextChoices):
        VIRTUAL = "virtual", "Virtual karta"
        PHYSICAL = "physical", "Physical karta"

    card_number = models.CharField(max_length=True, unique=True)
    card_holder_name = models.CharField(max_length=100)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="cards")

    expiry_month = models.PositiveSmallIntegerField()
    expiry_year = models.PositiveSmallIntegerField()

    card_type = models.CharField(
        mex_length=8, choices=CARD_TYPE.choices, default=CARD_TYPE.virtaul
    )

    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "cards"

    @property
    def masked_number(self):
        n = self.card_number
        return f"**** **** **** {n[-4:]}"

    @staticmethod
    def generate_card_number() -> str:
        prefix = "8600"
        remaining = "".join([str(randint(0, 9)) for _ in range(11)])
        partial = prefix + remaining
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

    @staticmethod
    def create_for_wallet(cls, wallet, holder_name: str, years_valid: int = 4):
        today = date.today()

        while True:
            card_number = cls.generate_card_number()
            if not cls.objects.filter(card_number=card_number).exists():
                break

        return cls.objects.create(
            card_number=card_number,
            wallet=wallet,
            card_holder_name=holder_name.upper(),
            expiry_month=today.month,
            expiry_year=today.year + years_valid,
        )
