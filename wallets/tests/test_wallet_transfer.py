from django.test import TestCase

from bankaccounts.factories import BankAccountFactory
from transactions.exceptions import TransactionException
from transactions.models import Transaction

class BankAccountTransferTestCase(TestCase):

    def test_negative_amount(self):
        bankaccount_out = BankAccountFactory(balance=5000)
        bankaccount_in = BankAccountFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(-55, bankaccount_in)
        self.assertRaises(TransactionException)

    def test_transfer_output(self):
        bankaccount_out = BankAccountFactory(balance=5000)
        bankaccount_in = BankAccountFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(55, bankaccount_in)
        self.assertIsInstance(transaction_in,Transaction)
        self.assertIsInstance(transaction_out, Transaction)

    def test_credit_transaction(self):
        bankaccount_out = BankAccountFactory(balance=5000)
        bankaccount_in = BankAccountFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(58, bankaccount_in)
        self.assertEqual(int(transaction_out.value), -58)

    def test_debit_transaction(self):
        bankaccount_out = BankAccountFactory(balance=5000)
        bankaccount_in = BankAccountFactory(balance=0)
        transaction_out, transaction_in = bankaccount_out.transfer(58, bankaccount_in)
        self.assertEqual(int(transaction_in.value), 58)


