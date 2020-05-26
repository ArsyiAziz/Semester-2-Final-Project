import tkinter as tk
from com.bankingsystem.database.Portal import Portal

LARGE_FONT = ("Verdana", 12)

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
    login_page.account_number.set('')
    portal.login(bank_names.index(current_bank_name.get()), account_number, password)
    if portal.login(bank_names.index(current_bank_name.get()), account_number, password):
        controller.show_frame(BankPage)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, text="Login to:", font=LARGE_FONT)
        self.label.pack()
        self.bni_btn = tk.Button(self, text="BNI",
                                 command=lambda: change_bank(controller, 0)).pack()
        self.bri_btn = tk.Button(self, text="BRI",
                                 command=lambda: change_bank(controller, 1)).pack()
        self.btn_btn = tk.Button(self, text="BTN",
                                 command=lambda: change_bank(controller, 2)).pack()
        self.mandiri_btn = tk.Button(self, text="MANDIRI",
                                     command=lambda: change_bank(controller, 3)).pack()

        global current_bank_name
        current_bank_name = tk.StringVar()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).grid(row=0)

        self.usernameLabel = tk.Label(self, text="Account Number").grid(row=1, column=0)
        self.account_number = tk.StringVar()
        self.usernameEntry = tk.Entry(self, textvariable=self.account_number).grid(row=1, column=1)

        # password label and password entry box
        self.passwordLabel = tk.Label(self, text="Password").grid(row=2, column=0)
        self.password = tk.StringVar()
        self.passwordEntry = tk.Entry(self, textvariable=self.password, show='*').grid(row=2, column=1)
        # login button
        self.back_btn = tk.Button(self, text="Back",
                                  command=lambda: controller.show_frame(StartPage)).grid(row=3, column=0)
        loginButton = tk.Button(self, text="Login",
                                command=lambda: login(controller, self)).grid(row=3, column=1)


class BankPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.label = tk.Label(self, textvariable=current_bank_name, font=LARGE_FONT).grid(row=0)

        self.logout_btn = tk.Button(self, text="Logout",
                                    command=lambda: controller.show_frame(StartPage)).grid(row=3, column=0)
