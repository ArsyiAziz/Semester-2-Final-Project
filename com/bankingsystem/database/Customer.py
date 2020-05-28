from com.bankingsystem.transactionlog.TransactionLog import *


def update_transactions(customer, transaction):
    if transaction.recipient_origin is None:
        transaction.recipient_origin = ''
    with open(f'Banks/{customer.get_bank()}/Customers/{customer.get_account_number()}.txt', 'r') as file:
        data = file.readlines()
        if len(data) == 1:
            data += '\n'
    data.append(
        format(
            f'{transaction.get_code()};{transaction.date_of_transaction};{transaction.amount};{transaction.recipient_origin};\n'))
    with open(f'Banks/{customer.get_bank()}/Customers/{customer.get_account_number()}.txt', 'w') as file:
        file.writelines(data)


class Customer():
    def __init__(self, username, password, account_number, ktp_number, transaction_log, balance, bank):
        super().__init__()
        self.__username = username
        self.__password = password
        self.__account_number = account_number
        self.__ktp_number = ktp_number
        self.__balance = balance
        self.__transaction_log = transaction_log
        self.__bank = bank
        self.__authenticated = False

    def get_bank(self):
        return self.__bank

    def get_ktp(self):
        if self.__authenticated:
            return self.__ktp_number

    def get_balance(self):
        if self.__authenticated:
            return self.__balance

    def login(self, password):
        if password == self.__password:
            self.__authenticated = True
            return True
        else:
            return False

    def get_name(self):
        if self.__authenticated:
            return self.__username

    def deposit(self, amount):
        if self.__authenticated:
            self.__balance += amount
            self.__update_transaction_log(Deposit(None, amount))

    def withdraw(self, amount):
        if self.__authenticated and self.__balance >= amount:
            self.__balance -= amount
            self.__update_transaction_log(Withdrawal(None, amount))
            return True
        else:
            return False

    def logout(self):
        self.__authenticated = False

    def __str__(self):
        return self.__account_number

    def outbound_transfer(self, amount, recipient):
        if self.__authenticated and self.__balance >= amount and recipient is not None:
            self.__balance -= amount
            self.__update_transaction_log(OutboundTransfer(None, amount, recipient.get_account_number()))
            recipient.__inbound_transfer(amount, self.__account_number)
            return True

    def __inbound_transfer(self, amount, origin):
        self.__balance += amount
        self.__update_transaction_log(InboundTransfer(None, amount, origin))

    def __update_transaction_log(self, transaction):
        self.__transaction_log.append(transaction)
        update_transactions(self, transaction)

    def __is_authenticated(self):
        return self.__authenticated

    def change_password(self, old_password, new_password):
        if self.__authenticated and old_password == self.__password:
            self.__password = new_password
            return True
        else:
            return False

    def get_account_number(self):
        return self.__account_number

    def get_transaction_log(self):
        if self.__authenticated:
            return self.__transaction_log
