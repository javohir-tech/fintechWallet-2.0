import random
from django.db import models
from shared.models import BaseModel


class Card(BaseModel):

    class CardType(models.TextChoices):
        VIRTUAL = "VIRTUAL", "Virtual Karta"
        PHYSICAL = "PHYSICAL", "Fizik Karta"

    wallet = models.ForeignKey(
        "wallets.Wallet",
        on_delete=models.CASCADE,
        related_name="cards"
    )

    # 16 xonali karta raqami — unique, DB indexed
    card_number = models.CharField(max_length=16, unique=True, db_index=True)

    # Ko'rsatish uchun formatlangan: **** **** **** 1234
    card_holder_name = models.CharField(max_length=100)

    expiry_month = models.PositiveSmallIntegerField()  # 1-12
    expiry_year = models.PositiveSmallIntegerField()   # 2025, 2026...

    card_type = models.CharField(
        max_length=10,
        choices=CardType.choices,
        default=CardType.VIRTUAL
    )
    is_active = models.BooleanField(default=True)
    is_primary = models.BooleanField(default=False)  # Asosiy karta

    class Meta:
        db_table = "cards"

    def __str__(self):
        return f"{self.masked_number} ({self.wallet.user})"

    @property
    def masked_number(self) -> str:
        """**** **** **** 1234 formatida"""
        n = self.card_number
        return f"**** **** **** {n[-4:]}"

    @staticmethod
    def generate_card_number() -> str:
        """
        Luhn algoritmiga asoslangan 16 xonali raqam.
        Birinchi raqam: 8 (O'zbekiston banklari odatda shu prefixdan foydalanadi)
        """
        prefix = "8600"  # Masalan: Uzcard prefix
        remaining = "".join([str(random.randint(0, 9)) for _ in range(11)])
        partial = prefix + remaining
        check_digit = Card._luhn_check_digit(partial)
        return partial + str(check_digit)

    @staticmethod
    def _luhn_check_digit(number: str) -> int:
        """Luhn algoritmi — karta raqami validatsiyasi"""
        digits = [int(d) for d in number]
        digits.reverse()
        total = 0
        for i, digit in enumerate(digits):
            if i % 2 == 0:
                doubled = digit * 2
                total += doubled - 9 if doubled > 9 else doubled
            else:
                total += digit
        return (10 - (total % 10)) % 10

    @classmethod
    def create_for_wallet(cls, wallet, holder_name: str, years_valid: int = 4):
        from datetime import date
        today = date.today()

        # Unique raqam generatsiya qilish
        while True:
            number = cls.generate_card_number()
            if not cls.objects.filter(card_number=number).exists():
                break

        return cls.objects.create(
            wallet=wallet,
            card_number=number,
            card_holder_name=holder_name.upper(),
            expiry_month=today.month,
            expiry_year=today.year + years_valid,
        )