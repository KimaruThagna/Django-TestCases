import mock
from django.core import mail
from django.test import TestCase, override_settings

from wallets.factories import DigitalWalletFactory
from transfer.factories import TransactionFactory


class TransactionNotificationLimitsTestCase(TestCase):
    @override_settings(TRANSACTION_NOTIFY_LIMIT_INBOUND=100)
    @override_settings(TRANSACTION_NOTIFY_LIMIT_OUTBOUND=-50)
    @mock.patch("wallets.models.WalletOwner.notify_about_transaction")
    
    def test_signal_limit_outbound(self, notify_mock):
        wallet_out = DigitalWalletFactory(balance=5000)
        wallet_in = DigitalWalletFactory(balance=0)

        # transfer the money
        transaction_out, transaction_in = wallet_out.transfer(50, wallet_in)

        # the notification function must have been called with the right transaction
        notify_mock.assert_called_once_with(transaction=transaction_out)

    @override_settings(TRANSACTION_NOTIFY_LIMIT_INBOUND=100)
    @override_settings(TRANSACTION_NOTIFY_LIMIT_OUTBOUND=-50)
    @mock.patch("wallets.models.WalletOwner.notify_about_transaction")
    def test_signal_limit_both(self, notify_mock):
        wallet_out = DigitalWalletFactory(balance=5000)
        wallet_in = DigitalWalletFactory(balance=0)

        # transfer the money
        transaction_out, transaction_in = wallet_out.transfer(100, wallet_in)

        # the notification function must have been called with the right transactions
        # order matters!
        notify_mock.assert_has_calls(
            [
                mock.call(transaction=transaction_out),
                mock.call(transaction=transaction_in),
            ]
        )

    @override_settings(TRANSACTION_NOTIFY_LIMIT_INBOUND=100)
    @override_settings(TRANSACTION_NOTIFY_LIMIT_OUTBOUND=-50)
    @mock.patch("wallets.models.WalletOwner.notify_about_transaction")
    def test_signal_limit_not_reached(self, notify_mock):
        wallet_out = DigitalWalletFactory(balance=5000)
        wallet_in = DigitalWalletFactory(balance=0)

        # transfer the money
        wallet_out.transfer(10, wallet_in)

        # notification function must not have been called
        notify_mock.assert_not_called()

    def test_notify_about_transaction(self):
        transaction = TransactionFactory(sender__owner__email="help@test.me")

        # clear outbox and send notification
        mail.outbox = []
        transaction.sender.owner.notify_about_transaction(transaction=transaction)

        # one message must be in the mail outbox
        self.assertEqual(len(mail.outbox), 1)

        # recipient must be the account owner
        self.assertEqual(mail.outbox[0].to, [transaction.sender.owner.email])
