from com.bankingsystem.transactionlog.Transaction import Transaction


class Deposit(Transaction):

    def __init__(self, date_of_transaction=None, amount=0):
        Transaction.__init__(self, date_of_transaction, amount )
        __transaction_type = "Deposit"

    def get_details(self):
        return "0;{};{}".format(self.date_of_transaction, self.amount)
