import datetime
from tkinter import *
import ПОКУПКИ_gui as Gui
import ПОКУПКИ_db as Db

root = Tk()
app = Gui.App(root)


class Terminal:
    def add_category(self, name):
        if name:
            Db.Categories.add(name)
            self.list_categories()

    def remove_category(self, name):
        Db.Categories.remove(name)
        self.list_categories()

    @staticmethod
    def add_spending(data):
        Db.Spendings.add(data)

    @staticmethod
    def remove_spending(uid):
        Db.Spendings.remove(uid)

    @staticmethod
    def list_categories():
        data = Db.Categories.get_all()
        app.page2.fill_categories(data)

    @staticmethod
    def list_spendings():
        data = Db.Spendings.get_all()
        app.page1.fill_spendings(data)


terminal = Terminal()
terminal.list_categories()
terminal.list_spendings()
root.mainloop()