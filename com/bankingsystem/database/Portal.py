import re

from com.bankingsystem.database.Database import Database


def is_valid_password(password):
    if 6 <= len(password) <= 12:
        if re.search("[a-z]", password) and re.search("[A-Z]", password):
            if re.search("[0-9]", password):
                return True
    return False


class Portal:
    __instance = None

    def __init__(self):
        if Portal.__instance is not None:
            raise Exception('Invalid class creation')
        else:
            Portal.__instance = self
            self.__database = Database.get_instance()
            self.current_bank = None
            self.current_customer = None

    @staticmethod
    def get_instance():
        if Portal.__instance is None:
            self.__instance = Portal()
        return Portal.__instance

    def set_bank(self, bank_index):
        self.current_bank = self.__database.get_bank(bank_index)

    def login(self, account_number, password):
        customer = self.current_bank.get_customer(account_number)
        if customer is None:
            return False
        if customer.login(password) != False:
            self.current_customer = self.current_bank.get_customer(account_number)
            return True
        else:
            return False

    def deposit(self, amount):
        self.current_customer.deposit(amount)

    def withdraw(self, amount):
        return self.current_customer.withdraw(amount)

    def change_password(self, old_password, new_password):
        if is_valid_password(new_password):
            is_successful = self.current_customer.change_password(old_password, new_password)
            if is_successful:
                self.__database.update_user_data(self.current_customer, new_password)
                return True

    def logout(self):
        self.current_customer.logout()
        self.current_customer = None
        self.current_bank = None

    def __valid_ktp(self, ktp):
        ktp = int(ktp)
        return self.current_bank.valid_ktp(ktp)

    def transfer(self, amount, destination):
        bank_index = int(str(destination)[0])-1
        try:
            recipient = self.__database.get_bank(bank_index).get_customer(destination)
        except AttributeError:
            pass
        return self.current_customer.outbound_transfer(amount, recipient)

    def register_customer(self, ktp, fullname, password):
        if self.__valid_ktp(ktp) and is_valid_password(password):
            self.current_customer = self.current_bank.register_customer(ktp, fullname, password)
            self.current_customer.login(password)
            self.__database.add_user(self.current_customer, password)
            return True
