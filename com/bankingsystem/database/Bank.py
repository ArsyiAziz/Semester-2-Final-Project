from com.bankingsystem.database.Customer import Customer


class Bank:
    def __init__(self, bank_name, bank_code, customers, registered_ktp):
        self.__bank_name = bank_name
        self.__bank_code = bank_code
        self.__customers = customers
        self.__registered_ktp = registered_ktp

    def __add_customer(self, username, password, account_number, ktp_number):
        self.__customers.put(account_number,
                             Customer(username, password, account_number, ktp_number, [], 0, self.__bank_name))

    def __register_customer(self, database):
        try:
            pass
        except IndexError:
            return False

    def __is_valid_password(self, password):
        return password >= 6

    def _get_bank_name(self):
        return self.__bank_name

    def _get_customer(self, account_number):
        return self.__customers.get(account_number)

