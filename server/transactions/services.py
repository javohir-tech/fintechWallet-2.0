from django.db import transaction as db_transaction
from .models import Transaction
from wallet.models import Wallet


def create_transfer(
    from_wallet: Wallet, to_wallet: Wallet, amount, idempotency_key, description=""
):

    existing = Transaction.objects.filter(idempotency_key=idempotency_key).first()

    if existing:
        return existing, False

    with db_transaction.atomic():
        wallets = Wallet.objects.select_for_update().filter(
            id__in=[from_wallet.id, to_wallet.id]
        ).order_by("id")

        sender: Wallet = next(w for w in wallets if w.id == from_wallet.id)
        reciver: Wallet = next(w for w in wallets if w.id == to_wallet.id)

        if not sender.has_enough_balance(amount):
            raise ValueError("Balans yetarli emas")

        tx = Transaction.objects.create(
            txtype=Transaction.TxType.TRANSFER,
            status=Transaction.TxStatus.PENDING,
            amount=amount,
            from_wallet=from_wallet,
            to_wallet=to_wallet,
            idempotency_key=idempotency_key,
            description=description,
            debit_amount=-amount,
            credit_amount=+amount,
        )

        sender.debit(amount)
        reciver.credit(amount)

        tx.status = Transaction.TxStatus.SUCCESS
        tx.save(update_fields=["status", "updated_time"])

    return tx, True
