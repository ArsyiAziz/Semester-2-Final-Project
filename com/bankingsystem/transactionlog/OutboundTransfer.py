from com.bankingsystem.transactionlog.Transaction import Transaction


class OutboundTransfer(Transaction):

    def __init__(self, date_of_transaction=None, amount=0, recipient_origin=None):
        Transaction.__init__(self, amount, date_of_transaction, recipient_origin)
        __transaction_type = "Outbound Transfer"

    def get_details(self):
        return "2;{};{}".format(self.date_of_transaction, self.amount)
