from com.bankingsystem.transactionlog.Transaction import Transaction


class Withdrawal(Transaction):
    __transaction_type = "Withdrawal"

    def __init__(self, amount, date_of_transaction=None):
        super().__init__(self, amount, date_of_transaction)


    def get_details(self):
        return "1;{};{}".format(self.date_of_transaction, self.amount)
