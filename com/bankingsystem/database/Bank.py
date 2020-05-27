from com.bankingsystem.database.Customer import Customer


class Bank:
    def __init__(self, bank_name, bank_code, customers, registered_ktp):
        self.__bank_name = bank_name
        self.__bank_code = bank_code
        self.__customers = customers
        self.__registered_ktp = registered_ktp

    def __add_customer(self, username, password, account_number, ktp_number):
        self.__customers[account_number] = Customer(username, password, account_number, ktp_number, [], 0, self.__bank_name)
        self.__registered_ktp.add(int(ktp_number))
        return self.__customers[account_number]

    def __str__(self):
        return self.__bank_name

    def register_customer(self, ktp_number, fullname, password):
        account_number = int(format(f'{self.__bank_code}{str(len(self.__customers) + 1).zfill(6)}'))
        return self.__add_customer(fullname, password, account_number, ktp_number)

    def valid_ktp(self, ktp_number):
        if ktp_number not in self.__registered_ktp:
            return True
        else:
            return False

    def get_bank_name(self):
        return self.__bank_name

    def get_customer(self, account_number):
        try:
            return self.__customers[account_number]
        except KeyError:
            return None
