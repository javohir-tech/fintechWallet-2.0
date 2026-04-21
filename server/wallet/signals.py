from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import Wallet


@receiver(post_save, sender=User)
def create_wallet_on_verify(sender, instance: User, created, **kwargs):

    if not created and instance.is_verified:
        Wallet.objects.get_or_create(
            user=instance,
        )
        
    
