from com.bankingsystem.transactionlog.Transaction import Transaction


class InboundTransfer(Transaction):
    __transaction_type = "Inbound Transfer"

    def __init__(self, amount, recipient_origin, date_of_transaction=None):
        super().__init__(self, amount, recipient_origin, date_of_transaction)


    def get_details(self):
        return "4;{};{}".format(self.date_of_transaction, self.amount)
