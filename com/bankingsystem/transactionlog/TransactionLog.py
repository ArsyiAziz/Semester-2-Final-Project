from datetime import datetime


class Transaction:
    codes = ['Deposit', 'Withdrawal', 'Inbound Transfer', 'Outbound Transfer']

    def __init__(self, transaction_type, date_of_transaction, amount, recipient_origin=None):
        self.transaction_type = transaction_type
        self.recipient_origin = recipient_origin
        if date_of_transaction is None:
            self.date_of_transaction = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        else:
            self.date_of_transaction = date_of_transaction
        self.amount = amount

    def get_code(self):
        return self.codes.index(self.transaction_type)

    def __str__(self):
        data = format(f"Date : {self.date_of_transaction}\n")
        data += format(f"Transaction Type : {self.transaction_type}\n")
        data += format(f"Amount : {self.amount}\n")
        if self.__transaction_type == "Outbound Transfer\n":
            data += format(f"To : {self.recipient_origin}")
        elif self.__transaction_type == "Inbound Transfer\n":
            data += format(f"From : {self.recipient_origin}")
        return data


class Withdrawal(Transaction):

    def __init__(self, date_of_transaction, amount):
        Transaction.__init__(self, "Withdrawal", date_of_transaction, amount)

    def get_details(self):
        return "1;{};{}".format(self.date_of_transaction, self.amount)


class OutboundTransfer(Transaction):

    def __init__(self, date_of_transaction, amount, recipient_origin):
        Transaction.__init__(self, "Outbound Transfer", date_of_transaction, amount, recipient_origin)
        self.code = None

    def get_details(self):
        return "2;{};{}".format(self.date_of_transaction, self.amount)


class InboundTransfer(Transaction):

    def __init__(self, date_of_transaction, amount, recipient_origin):
        Transaction.__init__(self, "Inbound Transfer", date_of_transaction, amount, recipient_origin)

    def get_details(self):
        return "4;{};{}".format(self.date_of_transaction, self.amount)


class Deposit(Transaction):

    def __init__(self, date_of_transaction, amount):
        Transaction.__init__(self, "Deposit", date_of_transaction, amount)

    def get_details(self):
        return "0;{};{}".format(self.date_of_transaction, self.amount)
