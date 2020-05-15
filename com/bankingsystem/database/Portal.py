from tkinter import *

from com.bankingsystem.database.Database import Database


class Portal:
    __instance = None

    def __init__(self):
        if Portal.__instance is not None:
            raise Exception('Invalid class creation')
        else:
            Portal.__instance = self
            __database = Database()

    @staticmethod
    def get_instance():
        if Portal.__instance is None:
            __instance = Portal()
        return Portal.__instance

    def login(self):
        pass
    def logout(self):
        pass

    def interface(self):
        master = Tk()
        master.title('Banking System 9000')
        canvas = Scale(master, from_=0, to=42)
        canvas.pack()
        button = Button(master, text='Stop', width=25, command=master.destroy)
        button.pack()
        master.mainloop()