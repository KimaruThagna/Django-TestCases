from django.db import models
from django.utils.translation import ugettext_lazy as _
from wallets.models import DigitalWallet


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

