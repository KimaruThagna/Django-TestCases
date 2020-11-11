class TransactionException(Exception):
    pass


class TransactionInsufficientFundsException(TransactionException):
    pass


class TransactionImmutableException(TransactionException):
    pass
