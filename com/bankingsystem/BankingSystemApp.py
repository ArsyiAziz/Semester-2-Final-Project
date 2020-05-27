import tkinter as tk

from com.bankingsystem.database.Pages import *


class BankingSystemApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        self.title("Banking System")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.resizable(width=False, height=False)
        self.frames = {}
        for F in (StartPage, LoginPage, BankPage, RegisterPage, DepositPage, WithdrawPage, TransferPage,
                  BalancePage, TransactionHistoryPage, ChangePasswordPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



app = BankingSystemApp()
app.mainloop()
