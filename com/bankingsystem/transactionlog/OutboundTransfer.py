from com.bankingsystem.transactionlog.Transaction import Transaction


class OutboundTransfer(Transaction):
    __transaction_type = "Outbound Transfer"

    def __init__(self, amount, recipient_origin, date_of_transaction=None):
        super().__init__(self, amount, recipient_origin, date_of_transaction)

    def get_details(self):
        return "2;{};{}".format(self.date_of_transaction, self.amount)
