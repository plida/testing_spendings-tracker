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
        
    def testGUICategoryAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        itemToAdd = 'item'

        app.make_page(page=app.page3)
        app.page3.add(itemToAdd)
        root.destroy()

        assert itemToAdd == testedDB.Categories.get_all()[0]

    def testGUIGainsAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        itemToAdd = ['item', 500, self.curr_date]
        for x in itemToAdd:
          if isinstance(x, str):
            x.strip()

        app.make_page(page=app.page2)
        app.page2.add(itemToAdd)
        root.destroy()

        assert itemToAdd == list(testedDB.Gains.get_all()[0][1:4])

    def testGUISpendingsAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        testedDB.Categories.add('a')
        testedDB.Gains.add(['salary', 5000, self.curr_date])

        itemToAdd = ['item', 'a', 500, self.curr_date]
        for x in itemToAdd:
          if isinstance(x, str):
            x.strip()

        app.make_page(page=app.page2)
        app.page1.add(itemToAdd)
        root.destroy()

        assert itemToAdd == list(testedDB.Spendings.get_all()[0][1:5])

    def testGUIDisplayCategoryAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        itemToAdd = 'item'

        app.make_page(page=app.page3)
        app.page3.add(itemToAdd)
        guiDisplay = app.page3.listbox.get(0, END)
        root.destroy()
        
        listedItem = guiDisplay[0]

        assert listedItem == itemToAdd

    def testGUIDisplayGainsAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        itemToAdd = ['item', 500, self.curr_date]

        app.make_page(page=app.page2)
        app.page2.add(itemToAdd)
        guiDisplay = list(app.page2.listbox.get(0, END))
        root.destroy()
        
        id, name, price, date = guiDisplay[0].split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()

        listedItem = [name, float(price), date]

        assert listedItem == itemToAdd

    def testGUIDisplaySpendingsAdd(self):
        root = Tk()
        app = testedGUI.App(root)

        testedDB.Categories.add('a')
        testedDB.Gains.add(['salary', 5000, self.curr_date])

        itemToAdd = ['item', 'a', 500, self.curr_date]
        for x in itemToAdd:
          if isinstance(x, str):
            x.strip()

        app.make_page(page=app.page2)
        app.page1.add(itemToAdd)
        guiDisplay = list(app.page1.listbox.get(0, END))
        root.destroy()
        
        id, name, category, price, date = guiDisplay[0].split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        listedItem = [name, category, float(price), date]

        assert listedItem == itemToAdd
    
        
if __name__ == '__main__':
    unittest.main()
