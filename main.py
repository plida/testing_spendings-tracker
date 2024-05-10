import datetime
from tkinter import *
import gui
import db

root = Tk()
app = gui.App(root)


class Terminal:
    def add_category(self, name):
        if name:
            db.Categories.add(name)
            self.list_categories()

    def remove_category(self, name):
        db.Categories.remove(name)
        self.list_categories()

    @staticmethod
    def add_spending(data):
        db.Spendings.add(data)

    @staticmethod
    def remove_spending(uid):
        db.Spendings.remove(uid)

    @staticmethod
    def list_categories():
        data = db.Categories.get_all()
        app.page2.fill_categories(data)

    @staticmethod
    def list_spendings():
        data = db.Spendings.get_all()
        app.page1.fill_spendings(data)


terminal = Terminal()
terminal.list_categories()
terminal.list_spendings()
root.mainloop()
