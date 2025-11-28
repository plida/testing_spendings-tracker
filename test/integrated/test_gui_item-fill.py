from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *

import datetime
import unittest

class testAddition(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2025, 11, 26)
        testedDB.initiate("test/integrated/spendings.db")
        self.clearData(testedDB.initSessions())

    def clearData(self, session):
        meta = testedDB.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def testGUIFillCategories(self):
        root = Tk()
        app = testedGUI.App(root)

        itemToAdd = 'item'

        testedDB.Categories.add(itemToAdd)

        app.make_page(page=app.page3)
        app.page3.fill(testedDB.Categories.get_all())
        guiDisplay = app.page3.listbox.get(0, END)
        root.destroy()
        
        listedItem = guiDisplay[0]

        assert listedItem == itemToAdd

    def testGUIFillGains(self):
        itemToAdd = ['item', 500, self.curr_date]
        testedDB.Gains.add(itemToAdd)

        root = Tk()
        app = testedGUI.App(root)

        app.make_page(page=app.page2)
        app.page2.fill(testedDB.Gains.get_all())
        guiDisplay = list(app.page2.listbox.get(0, END))
        root.destroy()
        
        id, name, price, date = guiDisplay[0].split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()

        listedItem = [name, float(price), date]

        assert listedItem == itemToAdd

    def testGUIFillSpendings(self):
        testedDB.Categories.add('a')
        testedDB.Gains.add(['salary', 5000, self.curr_date])
        itemToAdd = ['item', 'a', 100, self.curr_date]

        for x in itemToAdd:
          if isinstance(x, str):
            x.strip()
        testedDB.Spendings.add(itemToAdd)

        root = Tk()
        app = testedGUI.App(root)
        app.make_page(page=app.page1)

        app.page1.fill(testedDB.Spendings.get_all())
        guiDisplay = list(app.page1.listbox.get(0, END))
        root.destroy()
        
        id, name, category, price, date = guiDisplay[0].split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        listedItem = [name, category, float(price), date]

        assert listedItem == itemToAdd
    
        
if __name__ == '__main__':
    unittest.main()
