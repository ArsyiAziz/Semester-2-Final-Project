import glob
import os
import traceback

from com.bankingsystem.database.Bank import Bank
from com.bankingsystem.database.Customer import Customer
from com.bankingsystem.transactionlog.TransactionLog import *





class Database:
    __instance = None

    @staticmethod
    def get_instance():
        if Database.__instance is None:
            Database()
        return Database.__instance

    def __init__(self):
        if Database.__instance is not None:
            raise Exception('Invalid class creation')
        else:
            Database.__instance = self
            self.error_log = []
            self.banks = []
            self.__put_banks()

    def get_bank(self, index):
        return self.banks[index]

    def getBanks(self):
        return self.banks

    def print_error_log(self):
        if len(self.error_log) > 0:
            print('Successfully Loaded')
        else:
            print('Errors:')

        for error in self.error_log:
            print(error)

    def update_user_data(self, customer, password):
        with open(f'Banks/{customer.get_bank()}/Customers/{customer.get_account_number()}.txt', 'r') as file:
            data = file.readlines()
        data[0] = format(f'{customer.get_name()};{password};{customer.get_account_number()};{customer.get_ktp()};\n')

        with open(f'Banks/{customer.get_bank()}/Customers/{customer.get_account_number()}.txt', 'w') as file:
            file.writelines(data)

    def add_user(self, customer, password):
        with open(f'Banks/{customer.get_bank()}/Customers/{customer.get_account_number()}.txt', 'w') as file:
            file.writelines(
                format(f'{customer.get_name()};{password};{customer.get_account_number()};{customer.get_ktp()};\n'))

    def __put_banks(self):
        bank_names = ('BNI', 'BRI', 'BTN', 'MANDIRI')
        for bank in bank_names:
            bank_code = 0
            registered_ktp = {0}
            bank_name = None
            with open(f'Banks/{bank}/info.txt') as bf:
                try:
                    temp = bf.readline().split(';')
                    bank_name = temp[0]
                    bank_code = int(temp[1])
                    customers = {}
                    for filename in glob.glob(os.path.join(f'Banks/{bank}/Customers', '*.txt')):
                        with open(filename, 'r') as cf:
                            transaction_log = []
                            money = 0
                            cnt = 0
                            corrupted = False
                            customer_data = []
                            for line in cf:
                                if cnt == 0:
                                    customer_data = line.split(';')
                                    registered_ktp.add(int(customer_data[3]))
                                else:
                                    temp = line.split(';')
                                    if len(temp) < 2:
                                        print('here')
                                        continue
                                    if int(temp[0]) == 0:
                                        # Deposit
                                        transaction_log.append(Deposit(temp[1], temp[2]))
                                        money += int(temp[2])
                                    elif int(temp[0]) == 1:
                                        # Withdrawal
                                        transaction_log.append(Withdrawal(temp[1], int(temp[2])))
                                        money -= int(temp[2])
                                    elif int(temp[0]) == 2:
                                        # Inbound Transfer
                                        transaction_log.append(
                                            InboundTransfer(temp[1], int(temp[2]), temp[3]))
                                        money += int(temp[2])
                                    elif int(temp[0]) == 3:
                                        # Outbound Transfer
                                        transaction_log.append(
                                            OutboundTransfer(temp[1], int(temp[2]), temp[3]))
                                        money -= int(temp[2])
                                    else:
                                        error_log.append(f"{filename} is corrupted")
                                        corrupted = True
                                cnt += 1
                            if not corrupted:
                                customers[int(customer_data[2])] = Customer(customer_data[0],
                                                                            customer_data[1],
                                                                            customer_data[2],
                                                                            customer_data[3],
                                                                            transaction_log, money,
                                                                            bank_name)
                    self.banks.append(Bank(bank_name, bank_code, customers, registered_ktp))
                except Exception as er:
                    self.error_log.append(f"{bank_name} is corrupted")
                    traceback.print_exc()
        self.print_error_log()


