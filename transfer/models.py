from django.db import models
from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .exceptions import (
    TransactionInsufficientFundsException,
    TransactionImmutableException,
)

class Transaction(models.Model):
    sender = models.ForeignKey(
        "wallets.DigitalWallet",
        verbose_name=_("Account"),
        null=True,
        on_delete=models.PROTECT,
        related_name="account",
    )
    recepient = models.ForeignKey(
        "wallets.DigitalWallet",
        verbose_name=_("Remote account"),
        on_delete=models.PROTECT,
        related_name="remote",
    )
    value = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Value")
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))

    def save(self, *args, **kwargs):
        if self.pk: # if the pk already exists, then the save is an edit
            raise TransactionImmutableException(
                _("An existing transaction cannot be modified")
            )
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.pk:
            raise TransactionImmutableException(
                _("An existing transaction cannot be deleted")
            )
        super().delete(*args, **kwargs)

@receiver(post_save, sender=Transaction)
def transaction_created_update_balance(sender, instance, created, **kwargs):
    # check available funds when transferring out
    if instance.value < 0 and instance.sender.balance < instance.value * -1:
        raise TransactionInsufficientFundsException(_("Insufficient funds"))

    # update account balance
    instance.sender.balance += instance.value
    instance.sender.save(update_fields=["balance"])


@receiver(post_save, sender=Transaction)
def transaction_created(sender, instance, created, **kwargs):
    if created:
        if instance.value >= int(settings.TRANSACTION_NOTIFY_LIMIT_INBOUND):
            # send notification to receiver of funds
            instance.recepient.owner.notify_about_transaction(instance)

        if instance.value <= int(settings.TRANSACTION_NOTIFY_LIMIT_OUTBOUND):
            # send notification to sender
            instance.sender.owner.notify_about_transaction(instance)

