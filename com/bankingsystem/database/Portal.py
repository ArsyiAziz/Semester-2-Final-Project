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

    def logout(self):
        self.current_customer.logout()
