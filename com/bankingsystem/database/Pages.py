import tkinter as tk
import time
from tkinter import ttk

from com.bankingsystem.database.Portal import Portal

LARGE_FONT = ("Verdana", 16)

portal = Portal()
bank_names = ["BNI", "BRI", "BTN", "MANDIRI"]




def change_bank(controller, current_bank):
    current_bank_name.set(bank_names[current_bank])
    controller.show_frame(LoginPage)


def login(controller, login_page):
    account_number = None
    password = login_page.password.get()
    try:
        account_number = int(login_page.account_number.get())
    except:
        pass
    login_page.password.set('')
    portal.login(bank_names.index(current_bank_name.get()), account_number, password)
    if portal.login(bank_names.index(current_bank_name.get()), account_number, password):
        login_page.account_number.set('')
        controller.frames[BankPage].customer_name.set('Hello, ' + portal.current_customer.get_name())
        controller.show_frame(BankPage)
    

def logout(controller, bank_page):
    portal.logout()
    portal.current_customer = None
    portal.current_bank = None
    bank_page.customer_name.set('')
    controller.show_frame(StartPage)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Login to:", font=LARGE_FONT).grid(row=0, column=1, sticky="nesw")
        self.bni_btn = tk.Button(self, text="BNI",
                                 command=lambda: change_bank(controller, 0)).grid(row=1, column=1, sticky="nesw")
        self.bri_btn = tk.Button(self, text="BRI",
                                 command=lambda: change_bank(controller, 1)).grid(row=2, column=1, sticky="nesw")
        self.btn_btn = tk.Button(self, text="BTN",
                                 command=lambda: change_bank(controller, 2)).grid(row=3, column=1, sticky="nesw")
        self.mandiri_btn = tk.Button(self, text="MANDIRI",
                                     command=lambda: change_bank(controller, 3)).grid(row=4, column=1, sticky="nesw")
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(2, weight=1)

        global customer_account_number
        customer_account_number = tk.StringVar()
        global current_bank_name
        current_bank_name = tk.StringVar()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).grid(row=0, column=1, sticky="nsew")

        self.usernameLabel = tk.Label(self, text="Account Number").grid(row=1, column=1, sticky="nsew")
        self.account_number = tk.StringVar()
        self.account_number_entry = tk.Entry(self, textvariable=self.account_number)
        self.account_number_entry.bind('<Return>', lambda event: login(controller, self))
        self.account_number_entry.grid(row=1, column=2)

        self.passwordLabel = tk.Label(self, text="Password").grid(row=2, column=1, sticky="nsew")
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.bind('<Return>', lambda event: login(controller, self))
        self.password_entry.grid(row=2, column=2, sticky="nsew")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: controller.show_frame(StartPage)).grid(row=4, column=1, sticky="nsew")
        self.login_btn = tk.Button(self, text="Login",
                                   command=lambda: login(controller, self)).grid(row=4, column=2, sticky="nsew")
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(3, weight=1)


class BankPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.customer_name = tk.StringVar()
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).pack()

        self.label = tk.Label(self, textvariable=self.customer_name).pack()
        self.deposit_btn = tk.Button(self, text="Deposit",
                                     command=lambda: logout(controller, self)).pack()
        self.withdraw_btn = tk.Button(self, text="Withdraw",
                                      command=lambda: logout(controller, self)).pack()
        self.transfer_btn = tk.Button(self, text="Transfer",
                                      command=lambda: logout(controller, self)).pack()
        self.balance_btn = tk.Button(self, text="Balance",
                                     command=lambda: logout(controller, self)).pack()
        self.transaction_history_btn = tk.Button(self, text="Transaction History",
                                                 command=lambda: logout(controller, self)).pack()

        self.change_password_btn = tk.Button(self, text="Change Password").pack()
        self.logout_btn = tk.Button(self, text="Logout",
                                    command=lambda: logout(controller, self)).pack()
