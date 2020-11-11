from django.db import models
from django.utils.translation import ugettext_lazy as _
from wallets.models import DigitalWallet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Transaction(models.Model):
    sender = models.ForeignKey(
        DigitalWallet,
        verbose_name=_("Account"),
        null=True,
        on_delete=models.PROTECT,
        related_name="account",
    )
    recepient = models.ForeignKey(
        DigitalWallet,
        verbose_name=_("Remote account"),
        on_delete=models.PROTECT,
        related_name="remote",
    )
    value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Value")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))


@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created, **kwargs):
    if created:
        if instance.value >= int(settings.TRANSACTION_NOTIFY_LIMIT_INBOUND):
            # send notification to receiver of funds
            instance.recepient.owner.notify_about_transaction(instance)

        if instance.value <= int(settings.TRANSACTION_NOTIFY_LIMIT_OUTBOUND):
            # send notification to sender
            instance.sender.owner.notify_about_transaction(instance)

