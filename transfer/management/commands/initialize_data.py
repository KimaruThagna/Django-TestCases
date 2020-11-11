from django.core.management.base import BaseCommand

from wallets.factories import DigitalWalletFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        account_one = DigitalWalletFactory(balance=10000)
        account_two = DigitalWalletFactory(balance=2000)

        account_one.transfer(amount=250, target=account_two)
        account_one.transfer(amount=100, target=account_two)
        account_two.transfer(amount=700, target=account_one)
