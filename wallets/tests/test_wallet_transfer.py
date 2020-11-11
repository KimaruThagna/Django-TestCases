from django.test import TestCase

from wallets.factories import DigitalWalletFactory
from transfer.exceptions import TransactionInsufficientFundsException
from transfer.models import Transaction

class WalletTransferTestCase(TestCase):

    def test_negative_amount(self):
        bankaccount_out = DigitalWalletFactory(balance=5000)
        bankaccount_in = DigitalWalletFactory(balance=0)
        with self.assertRaises(TransactionInsufficientFundsException):
            transaction_out, transaction_in = bankaccount_out.transfer(-55, bankaccount_in)

    def test_transfer_output(self):
        bankaccount_out = DigitalWalletFactory(balance=5000)
        bankaccount_in = DigitalWalletFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(55, bankaccount_in)
        self.assertIsInstance(transaction_in,Transaction)
        self.assertIsInstance(transaction_out, Transaction)

    def test_credit_transaction(self):
        bankaccount_out = DigitalWalletFactory(balance=5000)
        bankaccount_in = DigitalWalletFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(58, bankaccount_in)
        self.assertEqual(int(transaction_out.value), -58)

    def test_debit_transaction(self):
        bankaccount_out = DigitalWalletFactory(balance=5000)
        bankaccount_in = DigitalWalletFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(58, bankaccount_in)
        self.assertEqual(int(transaction_in.value), 58)


    def test_insufficient_funds(self):
        bankaccount_out = DigitalWalletFactory(balance=0)
        bankaccount_in = DigitalWalletFactory(balance=0)
        with self.assertRaisesMessage(TransactionInsufficientFundsException,'Insufficient funds'):
            transaction_out, transaction_in = bankaccount_out.transfer(58, bankaccount_in)