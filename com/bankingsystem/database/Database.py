import glob
import os
from typing import final

from com.bankingsystem.database.Customer import Customer
from com.bankingsystem.transactionlog.Deposit import Deposit
from com.bankingsystem.transactionlog.Withdrawal import Withdrawal
from com.bankingsystem.transactionlog.InboundTransfer import InboundTransfer
from com.bankingsystem.transactionlog.OutboundTransfer import OutboundTransfer

class Database:
    __instance = None
    banks = []
    error_log = []

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
            self.__put_banks()



    @final
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
                    customers = []
                    for filename in glob.glob(os.path.join(f'Banks/{bank}/Customers', '*.txt')):
                        with open(filename, 'r') as cf:
                            customer_data = []
                            transaction_log = []
                            money = 0
                            cnt = 0
                            corrupted = False
                            for line in cf:
                                if cnt is 0:
                                    customer_data = line.split(';')
                                else:
                                    temp = line.split(';')
                                    if int(temp[0]) is 0:
                                        #Deposit
                                        transaction_log.append(Deposit(int(temp[1]),temp[2]))
                                        money += int(temp[1])
                                    elif int(temp[0]) is 1:
                                        #Withdrawal
                                        transaction_log.append(Withdrawal(int(temp[1]),temp[2]))
                                        money -= int(temp[1])
                                    elif int(temp[0]) is 2:
                                        # Outbound Transfer
                                        transaction_log.append(OutboundTransfer(int(temp[1]), int(temp[2]), temp[3]))
                                        money -= int(temp[1])
                                    elif int(temp[0]) is 2:
                                        # Inbound Transfer
                                        transaction_log.append(InboundTransfer(int(temp[1]), int(temp[2]), temp[3]))
                                        money += int(temp[1])
                                    else:
                                        self.error_log.append(f"{filename} is corrupted")
                                        corrupted = True
                                        registered_ktp.add(customer_data[3])
                            if not corrupted:
                                customers.append(Customer(customer_data[0], customer_data[1], customer_data[2], customer_data[3], transaction_log, money, bank_name))
                    self.banks.append(Bank(bank_name, bank_code, customers, registered_ktp))

                except IndexError:
                    self.error_log.append(f"{bank_name} is corrupted")

