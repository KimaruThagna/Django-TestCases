import factory
from factory import faker
from .models import *

class WalletOwnerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WalletOwner

    given_name = faker.Faker("first_name")
    family_name = faker.Faker("last_name")
    email = faker.Faker("email")


class DigitalWalletFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DigitalWallet

    owner = factory.SubFactory("wallets.factories.WalletOwnerFactory")
    iban = faker.Faker("iban")
    balance = faker.Faker("pyint", min_value=0, max_value=100000)
