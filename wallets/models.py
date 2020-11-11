from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.transaction import atomic
from django.conf import settings
from django.core.mail import send_mail

from transfer.models import Transaction

class WalletOwner(models.Model):
    given_name = models.CharField(max_length=50, verbose_name=_("Given name"))
    family_name = models.CharField(max_length=50, verbose_name=_("Family name"))
    email = models.EmailField(verbose_name=_("Email"))

    def __str__(self):
        return f'{self.given_name} {self.family_name}'

    def notify_about_transaction(self, transaction):
        send_mail(
            settings.NOTIFICATION_SUBJECT,
            f'This is to notify you of a transaction performed on{transaction.created} of value {transaction.value}',
            settings.DEFAULT_SENDER,
            [self.email],
            fail_silently=False,
        )


class DigitalWallet(models.Model):
    owner = models.ForeignKey(
        WalletOwner,
        verbose_name=_("Account owner"),
        on_delete=models.CASCADE,
    )
    iban = models.CharField(max_length=34, unique=True, verbose_name=_("IBAN"),)
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_("Balance")
    )

    @atomic
    def transfer(self, amount, target):
        # transfer amounts must be positive

        # get records locked for update
        source = self.get_locked()
        target = target.get_locked()

        transaction_out = Transaction.objects.create(
            sender=source, recepient=target, value=amount * -1
        )

        transaction_in = Transaction.objects.create(
            recepient=target, sender=source, value=amount
        )
        return transaction_out, transaction_in

    def get_locked(self):
        return DigitalWallet.objects.select_for_update().get(id=self.id)


    def __str__(self):
        return f'{self.owner.given_name} has {self.balance} digital coins'

