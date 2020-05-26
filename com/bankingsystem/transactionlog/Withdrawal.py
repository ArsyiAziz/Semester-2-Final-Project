from com.bankingsystem.transactionlog.Transaction import Transaction


class Withdrawal(Transaction):

    def __init__(self, date_of_transaction=None, amount=0):
        Transaction.__init__(self,  date_of_transaction, amount)
        __transaction_type = "Withdrawal"

    def get_details(self):
        return "1;{};{}".format(self.date_of_transaction, self.amount)
