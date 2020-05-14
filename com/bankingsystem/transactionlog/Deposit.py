from com.bankingsystem.transactionlog.Transaction import Transaction


class Deposit(Transaction):
    __transaction_type = "Deposit"

    def __init__(self, amount, date_of_transaction=None):
        super().__init__(self, amount, date_of_transaction)

    def get_details(self):
        return "0;{};{}".format(self.date_of_transaction, self.amount)
