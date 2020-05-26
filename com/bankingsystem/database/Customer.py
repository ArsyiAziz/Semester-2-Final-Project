
class Customer():
    def __init__(self, username, password, account_number, ktp_number, transaction_log, balance, bank):
        super().__init__()
        self.__username = username
        self.__password = password
        self.__account_number = account_number
        self.__ktp_number = ktp_number
        self.__balance = balance
        self.__transaction_log = list(transaction_log)
        self.__bank = bank
        self.__authenticated = False

    def get_bank(self):
        return bank

    def get_balance(self):
        if self.__authenticated:
            return self.__balance

    def login(self, password):
        if password == self.__password:
            self.__authenticated = True
            return True
        else:
            return False

    def deposit(self, amount):
        if self.__authenticated:
            self.__balance += amount
            self.__update_transaction_log(Deposit(amount))

    def withdraw(self, amount):
        if self.__authenticated and self.__balance >= amount:
            self.__balance -= amount
            self.__update_transaction_log(Withdrawal(amount))
            return True

    def logout(self):
        self.__authenticated = False

    def __str__(self):
        if self.__authenticated:
            return self.__account_number

    def outbound_transfer(self, amount, recipient):
        if self.__authenticated and self.__balance >= amount:
            self.__balance -= amount

            self.__update_transaction_log(Withdrawal(amount, recipient._get_account_number))
            return True

    def __update_transaction_log(self, transaction):
        self.__transaction_log.append(transaction)

    def __is_authenticated(self):
        return self.__authenticated

    def change_password(self, database):
        if self.__authenticated:
            tries = 3
            while tries >= 0:
                pass


    def get_account_number(self):
        return self.__account_number

    def get_transaction_log(self):
        if self.__authenticated:
            return self.__transaction_log


