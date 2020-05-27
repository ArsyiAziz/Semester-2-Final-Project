from com.bankingsystem.database.Database import Database


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

    def login(self, bank, account_number, password):
        try:
            self.current_bank = self.__database.get_bank(bank)
            if self.current_bank.get_customer(account_number).login(password):
                self.current_customer = self.current_bank.get_customer(account_number)
                return True
            else:
                return False
        except:
            pass

    def deposit(self, amount):
        self.current_customer.deposit(amount)

    def withdraw(self, amount):
        return self.current_customer.withdraw(amount)

    def change_password(self, old_password, new_password):
        is_successful = self.current_customer.change_password(old_password, new_password)
        if is_successful:
            self.__database.update_user_password(self.current_customer, new_password)
            return True
        else:
            return False

    def logout(self):
        self.current_customer.logout()
        self.current_customer = None
        self.current_bank = None
