import datetime
from tkinter import *
import gui
import db
import gui_new

root = Tk()
app = gui_new.App(root)


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
        app.page2.fill(data)

    @staticmethod
    def list_spendings():
        data = db.Spendings.get_all()
        app.page1.fill(data)

    @staticmethod
    def list_gains():
        data = db.Gains.get_all()
        app.page3.fill(data)

    @staticmethod
    def calculate_total():
        data1 = db.Spendings.get_all()
        data2 = db.Gains.get_all()
        sm = 0
        for row in data1:
            sm -= row[3]
        for row in data2:
            sm += row[2]
        app.totalVAR.set(sm)

    @staticmethod
    def calculate_month_spend():
        data1 = db.Spendings.get_all_recent()
        sm = 0
        for row in data1:
            sm += row[3]
        app.spendingsVAR.set(sm)

    @staticmethod
    def calculate_month_gain():
        data1 = db.Gains.get_all_recent()
        sm = 0
        for row in data1:
            sm += row[2]
        app.salaryVAR.set(sm)

terminal = Terminal()
terminal.list_categories()
terminal.list_spendings()
terminal.list_gains()
terminal.calculate_total()
terminal.calculate_month_spend()
terminal.calculate_month_gain()
root.mainloop()
