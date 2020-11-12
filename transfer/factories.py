import factory
from factory import faker
from .models import Transaction
from wallets.factories import DigitalWalletFactory

class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    sender = factory.SubFactory(DigitalWalletFactory)
    recepient = factory.SubFactory(DigitalWalletFactory)
    value = faker.Faker("pyint")
