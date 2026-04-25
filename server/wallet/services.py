from .models import Wallet
from decimal import Decimal
from django.db import transaction as db_transaction


def transfer_funds(from_wallet_id, to_wallet_id, amount: Decimal):

    with db_transaction.atomic():
        wallet = (
            Wallet.objects.select_for_update()
            .filter(id__in=[from_wallet_id, to_wallet_id])
            .order_by("id")
        )

        from_wallet = next(w for w in wallet if w.id == from_wallet_id)
        to_wallet = next(w for w in wallet if w.id == to_wallet_id)

        if not from_wallet.has_enough_balance(amount):
            raise ValueError("Balans yetarli emas")

        from_wallet.debit(amount)
        to_wallet.credit(amount)

        return amount
