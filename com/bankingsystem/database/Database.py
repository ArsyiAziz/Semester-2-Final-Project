import glob
import os
import traceback

from com.bankingsystem.database.Bank import Bank
from com.bankingsystem.database.Customer import Customer
from com.bankingsystem.transactionlog.Deposit import Deposit
from com.bankingsystem.transactionlog.Withdrawal import Withdrawal
from com.bankingsystem.transactionlog.InboundTransfer import InboundTransfer
from com.bankingsystem.transactionlog.OutboundTransfer import OutboundTransfer


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

    def __put_banks(self):
        self.bank_names = ('BNI', 'BRI', 'BTN', 'MANDIRI')
        for bank in self.bank_names:
            self.bank_code = 0
            self.registered_ktp = {0}
            self.bank_name = None
            with open(f'Banks/{bank}/info.txt') as bf:
                try:
                    self.temp = bf.readline().split(';')
                    self.bank_name = self.temp[0]
                    self.bank_code = int(self.temp[1])
                    self.customers = {}
                    for filename in glob.glob(os.path.join(f'Banks/{bank}/Customers', '*.txt')):
                        with open(filename, 'r') as cf:
                            self.transaction_log = []
                            self.money = 0
                            self.cnt = 0
                            self.corrupted = False
                            self.customer_data = []
                            for line in cf:
                                if self.cnt == 0:
                                    self.customer_data = line.split(';')
                                    self.customer_data.pop()
                                else:
                                    self.temp = line.split(';')
                                    self.temp.pop()
                                    if int(self.temp[0]) == 0:
                                        # Deposit
                                        self.transaction_log.append(Deposit(int(self.temp[1]), self.temp[2]))
                                        self.money += int(self.temp[1])
                                    elif int(self.temp[0]) == 1:
                                        # Withdrawal
                                        self.transaction_log.append(Withdrawal(int(self.temp[1]), self.temp[2]))
                                        self.money -= int(temp[1])
                                    elif int(self.temp[0]) == 2:
                                        # Outbound Transfer
                                        self.transaction_log.append(
                                            OutboundTransfer(int(self.temp[1]), int(self.temp[2]), self.temp[3]))
                                        self.money -= int(temp[1])
                                    elif int(temp[0]) == 2:
                                        # Inbound Transfer
                                        self.transaction_log.append(
                                            InboundTransfer(int(self.temp[1]), int(self.temp[2]), self.temp[3]))
                                        self.money += int(self.temp[1])
                                    else:
                                        self.error_log.append(f"{filename} is corrupted")
                                        self.corrupted = True
                                        self.registered_ktp.add(self.customer_data[3])
                                self.cnt += 1
                            if not self.corrupted:
                                print(self.customer_data)
                                self.customers[int(self.customer_data[2])] = Customer(self.customer_data[0],
                                                                                      self.customer_data[1],
                                                                                      self.customer_data[2],
                                                                                      self.customer_data[3],
                                                                                      self.transaction_log, self.money,
                                                                                      self.bank_name)
                    print(self.customers.keys())
                    self.banks.append(Bank(self.bank_name, self.bank_code, self.customers, self.registered_ktp))
                    print(f'Successfully Added {self.bank_name}')
                except Exception as err:
                    self.error_log.append(f"{self.bank_name} is corrupted")
                    print(f"{self.bank_name} is corrupted")
                    traceback.print_exc()
        self.print_error_log()
