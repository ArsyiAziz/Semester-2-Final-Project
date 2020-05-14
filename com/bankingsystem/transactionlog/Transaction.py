from datetime import datetime


class Transaction():

    def __init__(self, amount, recipient_origin=None, date_of_transaction=None):
        if date_of_transaction is None:
            self.date_of_transaction = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        else:
            self.date_of_transaction = date_of_transaction
        self.amount = amount
        if recipient_origin is not None:
            self.recipient_origin = recipient_origin

    def __str__(self):
        data = format(f"Date : {self.date_of_transaction}", )
        data += format(f"Transaction Type : {self.__transaction_type}", )
        data += format(f"Amount : {self.amount}")
        if self.__transaction_type is "Outbound Transfer":
            print(f"To : {self.recipient_origin}")
        elif self.__transaction_type is "Inbound Transfer":
            print(f"From : {self.recipient_origin}")

    def get_details(self):
        pass
