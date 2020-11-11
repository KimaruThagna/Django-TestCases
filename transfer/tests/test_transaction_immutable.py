from django.test import TestCase
from transactions.models import Transaction
from transactions.factories import TransactionFactory

from transactions.exceptions import (
    TransactionImmutableException,
)

class TransactionImmutableTestCase(TestCase):
    def test_create(self):
        """
        test that we can successfully create and store a new Transaction dataset
        """
        txn = TransactionFactory(account__owner__email="help@test.me", value=80)
        self.assertEqual(int(txn.value), 80)


    def test_change(self):
        """
        test that we cannot change a database-stored Transaction dataset
        """
        with self.assertRaises(TransactionImmutableException):
            txn = TransactionFactory(account__owner__email="help@test.me", value=80)
            txn.value = 86
            txn.save()


    def test_delete(self):
        """
        test that we cannot delete a database-stored Transaction dataset
        """

        with self.assertRaises(TransactionImmutableException):
            txn = TransactionFactory(account__owner__email="help@test.me", value=80)
            txn.delete()
