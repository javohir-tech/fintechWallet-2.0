from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, AuthStatus
from .models import Wallet
from cards.models import Card


@receiver(post_save, sender=User)
def create_wallet_on_verify(sender, instance: User, created, **kwargs):

    if instance.auth_status != AuthStatus.DONE:
        return

    wallet, _ = Wallet.objects.get_or_create(user=instance)

    if not Card.objects.filter(wallet=wallet).exists():
        Card.create_for_wallet(
            wallet,
            holder_name=instance.get_full_name() or instance.username,
            expiry_year=5,
        )