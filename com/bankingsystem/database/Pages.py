import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext

from PIL import ImageTk, Image
import os

from com.bankingsystem.database.Portal import Portal

LARGE_FONT = ("Verdana", 16)

portal = Portal()
bank_names = ["BNI", "BRI", "BTN", "MANDIRI"]
customer_balance = None


def register_customer(controller, register_page):
    ktp = register_page.ktp.get()
    fullname = register_page.fullname.get()
    password = register_page.password.get()
    is_successful = portal.register_customer(ktp, fullname, password)
    if is_successful:
        controller.frames[BankPage].customer_name.set('Hello, ' + portal.current_customer.get_name())
        controller.show_frame(BankPage)

def get_customer_balance():
    global customer_balance
    customer_balance.set('Rp. ' + str(portal.current_customer.get_balance()))
    return customer_balance


def change_bank(controller, current_bank):
    current_bank_name.set(bank_names[current_bank])
    controller.show_frame(LoginPage)
    portal.set_bank(current_bank)

def login(controller, login_page):
    account_number = None
    password = login_page.password.get()
    try:
        account_number = int(login_page.account_number.get())
    except:
        pass
    login_page.password.set('')
    logged_in = portal.login(account_number, password)
    if logged_in:
        login_page.account_number.set('')
        controller.frames[BankPage].customer_name.set('Hello, ' + portal.current_customer.get_name())
        controller.show_frame(BankPage)


def logout(controller):
    portal.logout()
    controller.show_frame(BankPage)


def change_password(controller, old_password, new_password, verify_password, change_password_page):
    if verify_password == new_password:
        is_successful = portal.change_password(old_password, new_password)
        if is_successful:
            change_password_page.new_password.set('')
            change_password_page.old_password.set('')
            change_password_page.verify_password.set('')
            controller.show_frame(BankPage)
        else:
            change_password_page.old_password.set('')


def deposit(controller, deposit_page):
    try:
        amount = int(deposit_page.amount.get())
        portal.deposit(amount)
    except ValueError:
        deposit_page.amount.set('Invalid amount!')
        return
    deposit_page.amount.set('')
    controller.show_frame(BankPage)


def withdraw(controller, withdraw_page):
    try:
        amount = int(withdraw_page.amount.get())
        is_successful = portal.withdraw(amount)
    except ValueError:
        withdraw_page.amount.set('Invalid amount!')
        return
    if is_successful:
        controller.show_frame(BankPage)
    else:
        withdraw_page.amount.set('Insufficient Funds!')


def transfer(controller, transfer_page):
    try:
        amount = int(transfer_page.amount.get())
        destination = int(transfer_page.destination.get())
    except ValueError:
        pass
    is_successful = portal.transfer(amount, destination)
    if is_successful:
        transfer_page.amount.set('')
        transfer_page.destination.set('')
        controller.show_frame(BankPage)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        global bni_logo, bri_logo, btn_logo, mandiri_logo
        bni_logo = ImageTk.PhotoImage(Image.open("Assets/Logos/bni.png").resize((130, 70)))
        bri_logo = ImageTk.PhotoImage(Image.open("Assets/Logos/bri.png").resize((130, 70)))
        btn_logo = ImageTk.PhotoImage(Image.open("Assets/Logos/btn.png").resize((100, 70)))
        mandiri_logo = ImageTk.PhotoImage(Image.open("Assets/Logos/mandiri.png").resize((120, 70)))
        global customer_balance
        customer_balance = tk.StringVar()

        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Login to:", font=LARGE_FONT).grid(row=1, column=1, sticky="nesw")
        self.bni_btn = tk.Button(self, text="BNI",
                                 command=lambda: change_bank(controller, 0)).grid(row=2, column=1, sticky="nesw")
        self.bri_btn = tk.Button(self, text="BRI",
                                 command=lambda: change_bank(controller, 1)).grid(row=3, column=1, sticky="nesw")
        self.btn_btn = tk.Button(self, text="BTN",
                                 command=lambda: change_bank(controller, 2)).grid(row=4, column=1, sticky="nesw")
        self.mandiri_btn = tk.Button(self, text="MANDIRI",
                                     command=lambda: change_bank(controller, 3)).grid(row=5, column=1, sticky="nesw")
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)

        global customer_account_number
        customer_account_number = tk.StringVar()
        global current_bank_name
        current_bank_name = tk.StringVar()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        global login_page
        login_page = self
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, textvariable=current_bank_name,
                              font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")

        self.usernameLabel = tk.Label(self, text="Account Number").grid(row=2, column=1, sticky="nsew")
        self.account_number = tk.StringVar()
        self.account_number_entry = tk.Entry(self, textvariable=self.account_number)
        self.account_number_entry.bind('<Return>', lambda event: login(controller, self))
        self.account_number_entry.grid(row=2, column=3)

        self.passwordLabel = tk.Label(self, text="Password").grid(row=3, column=1, sticky="nsew")
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.bind('<Return>', lambda event: login(controller, self))
        self.password_entry.grid(row=3, column=3, sticky="nsew")
        self.login_btn = tk.Button(self, text="Login",
                                   command=lambda: [login(controller, self)]).grid(row=4, column=3, sticky="nsew")
        self.register_btn = tk.Button(self, text="Register",
                                      command=lambda: controller.show_frame(RegisterPage)).grid(row=5, column=3,
                                                                                                sticky="nsew")
        self.back_btn = tk.Button(self, text="Back", bg='red',
                                  command=lambda: [controller.show_frame(StartPage),
                                                   self.account_number.set(''),
                                                   self.password.set('')]).grid(row=4, column=1, sticky="nsew")
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(9, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.ktp = tk.StringVar()
        self.fullname = tk.StringVar()
        self.password = tk.StringVar()
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).grid(row=1, column=1,
                                                                                          sticky="nsew")
        self.ktp_label = tk.Label(self, text="KTP Number").grid(row=3, column=1, sticky="nesw")
        self.ktp_entry = tk.Entry(self, textvariable=self.ktp).grid(row=3, column=2, sticky="nesw")
        self.fullname_label = tk.Label(self, text="Full Name").grid(row=4, column=1, sticky="nesw")
        self.fullname_entry = tk.Entry(self, textvariable=self.fullname).grid(row=4, column=2, sticky="nesw")
        self.password_label = tk.Label(self, text="Password").grid(row=5, column=1, sticky="nesw")
        self.password_entry = tk.Entry(self, textvariable=self.password).grid(row=5, column=2, sticky="nesw")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(LoginPage), self.ktp.set(''), self.password.set(''), self.fullname.set('')]).grid(row=6, column=1, sticky="nsew")
        self.register_btn = tk.Button(self, text="Register",
                                      command=lambda: register_customer(controller, self)).grid(row=6, column=2,
                                                                                                sticky="nsew")
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(0, weight=1)


class BankPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.customer_name = tk.StringVar()
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).grid(row=1, column=1,
                                                                                          sticky="nsew")
        self.label = tk.Label(self, textvariable=self.customer_name).grid(row=2, column=1, sticky="nsew")
        self.deposit_btn = tk.Button(self, text="Deposit",
                                     command=lambda: controller.show_frame(DepositPage)).grid(row=3, column=1,
                                                                                              sticky="nsew")
        self.withdraw_btn = tk.Button(self, text="Withdraw",
                                      command=lambda: controller.show_frame(WithdrawPage)).grid(row=4,
                                                                                                column=1, sticky="nsew")
        self.transfer_btn = tk.Button(self, text="Transfer",
                                      command=lambda: controller.show_frame(TransferPage)).grid(row=5,
                                                                                                column=1, sticky="nsew")
        self.balance_btn = tk.Button(self, text="Balance",
                                     command=lambda: [get_customer_balance(), controller.show_frame(BalancePage)]).grid(
            row=6,
            column=1, sticky="nsew")
        self.transaction_history_btn = tk.Button(self, text="Transaction History",
                                                 command=lambda:
                                                 controller.show_frame(TransactionHistoryPage)).grid(row=7, column=1,
                                                                                                     sticky="nsew")

        self.change_password_btn = tk.Button(self, text="Change Password",
                                             command=lambda:
                                             controller.show_frame(ChangePasswordPage)).grid(row=8,
                                                                                             column=1,
                                                                                             sticky="nsew")
        self.logout_btn = tk.Button(self, text="Logout",
                                    command=lambda: [logout(controller),
                                                     controller.show_frame(StartPage)]).grid(row=9,
                                                                                             column=1,
                                                                                             sticky="nsew")
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)


class DepositPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = tk.Label(self, text="Deposit", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")
        self.amount_label = tk.Label(self, text="Amount Rp.").grid(row=2, column=1, sticky="nsew")
        self.amount = tk.StringVar()
        self.amount_entry = tk.Entry(self, textvariable=self.amount).grid(row=2, column=2, sticky="nsew")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(BankPage),
                                                   self.amount.set('')]).grid(row=6, column=1, sticky="nsew")
        self.deposit_btn = tk.Button(self, text="Deposit",
                                     command=lambda: deposit(controller, self)).grid(row=6, column=2, sticky="nsew")
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)


class WithdrawPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Withdraw", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")
        self.amount = tk.StringVar()
        self.amount_label = tk.Label(self, text="Amount Rp.").grid(row=2, column=1, sticky="nesw")
        self.amount_entry = tk.Entry(self, textvariable=self.amount).grid(row=2, column=2, sticky="nesw")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(BankPage),
                                                   self.amount.set('')]).grid(row=6, column=1, sticky="nsew")
        self.withdraw_btn = tk.Button(self, text="Withdraw",
                                      command=lambda: withdraw(controller, self)).grid(row=6, column=2, sticky="nsew")
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)


class TransferPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Transfer", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")
        self.amount = tk.StringVar()
        self.amount_label = tk.Label(self, text="Amount Rp.").grid(row=2, column=1, sticky="nsew")
        self.amount_entry = tk.Entry(self, textvariable=self.amount).grid(row=2, column=2, sticky="nsew")
        self.destination = tk.StringVar()
        self.destination_label = tk.Label(self, text="Account Number").grid(row=3, column=1, sticky="nsew")
        self.destination_entry = tk.Entry(self, textvariable=self.destination).grid(row=3, column=2, sticky="nsew")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(BankPage),
                                                   self.amount.set('')]).grid(row=6, column=1, sticky="nsew")
        self.transfer_btn = tk.Button(self, text="Deposit",
                                     command=lambda: transfer(controller, self)).grid(row=6, column=2, sticky="nsew")
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)


class BalancePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Balance", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")
        self.label = tk.Label(self, textvariable=customer_balance, font=LARGE_FONT).grid(row=2, column=1, sticky="nsew")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(BankPage),
                                                   customer_balance.set('')]).grid(row=6, column=1, sticky="nsew")
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)


class TransactionHistoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Transaction History", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")


class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Change Password", font=LARGE_FONT).grid(row=1, column=1, sticky="nsew")
        self.old_password = tk.StringVar()
        self.old_password_label = tk.Label(self, text="Old Password").grid(row=2, column=1, sticky="nsew")
        self.old_password_entry = tk.Entry(self, textvariable=self.old_password, show='*')
        self.new_password = tk.StringVar()
        self.new_password_label = tk.Label(self, text="New Password").grid(row=3, column=1, sticky="nsew")
        self.new_password_entry = tk.Entry(self, textvariable=self.new_password, show='*')
        self.verify_password = tk.StringVar()
        self.verify_password_label = tk.Label(self, text="Verify Password").grid(row=4, column=1, sticky="nsew")
        self.verify_password_entry = tk.Entry(self, textvariable=self.verify_password, show='*')
        self.old_password_entry.bind('<Return>', lambda event: change_password(controller, self.old_password.get(),
                                                                               self.new_password.get(),
                                                                               self.verify_password.get(),
                                                                               self))
        self.new_password_entry.bind('<Return>', lambda event: change_password(controller, self.old_password.get(),
                                                                               self.new_password.get(),
                                                                               self.verify_password.get(),
                                                                               self))
        self.verify_password_entry.bind('<Return>', lambda event: change_password(controller, self.old_password.get(),
                                                                                  self.new_password.get(),
                                                                                  self.verify_password.get(),
                                                                                  self))
        self.old_password_entry.grid(row=2, column=2, sticky="nsew")
        self.new_password_entry.grid(row=3, column=2, sticky="nsew")
        self.verify_password_entry.grid(row=4, column=2, sticky="nsew")
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: [controller.show_frame(BankPage),
                                                   self.new_password.set(''), self.old_password.set(''),
                                                   self.verify_password.set('')]).grid(row=6, column=1, sticky="nsew")
        self.change_password_btn = tk.Button(self, text="Change Password",
                                             command=lambda: change_password(controller, self.old_password.get(),
                                                                             self.new_password.get(),
                                                                             self.verify_password.get(),
                                                                             self)).grid(row=6,
                                                                                         column=2,
                                                                                         sticky="nsew")
