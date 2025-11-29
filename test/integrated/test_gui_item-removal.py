from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *

import datetime
import unittest

class testItemRemove(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2025, 11, 26)
        testedDB.initiate("test/integrated/spendings.db")
        self.clearData(testedDB.initSessions())

    def clearData(self, session):
        meta = testedDB.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def testGUICategoryRemove(self):
        testedDB.Categories.add('1')
        testedDB.Categories.add('2')
        testedDB.Categories.add('3')

        root = Tk()
        app = testedGUI.App(root)
        app.page3.fill(testedDB.Categories.get_all())
        app.make_page(page=app.page3)

        app.page3.listbox.selection_set(1)
        app.page3.remove()
        
        root.destroy()
        
        assert len(testedDB.Categories.get_all()) == 2 and len(testedDB.Categories.get_all_filter('2')) == 0

    def testGUISpendingsRemove(self):
        testedDB.Categories.add('numbers')
        testedDB.Spendings.add(['1', 'numbers', 500, self.curr_date], self.curr_date)
        testedDB.Spendings.add(['2', 'numbers', 30, self.curr_date], self.curr_date)
        testedDB.Spendings.add(['3', 'numbers', 1, self.curr_date], self.curr_date)

        root = Tk()
        app = testedGUI.App(root)
        app.page1.fill(testedDB.Spendings.get_all())
        app.make_page(page=app.page1)

        app.page1.listbox.selection_set(1)
        app.page1.remove()
        
        root.destroy()
        assert len(testedDB.Spendings.get_all()) == 2 and len(testedDB.Spendings.get_all_filter(['2', 'numbers', 30, self.curr_date])) == 0

    def testGUIGainsRemove(self):
        testedDB.Gains.add(['1', 500, self.curr_date], self.curr_date)
        testedDB.Gains.add(['2', 30, self.curr_date], self.curr_date)
        testedDB.Gains.add(['3', 1, self.curr_date], self.curr_date)

        root = Tk()
        app = testedGUI.App(root)
        app.page2.fill(testedDB.Gains.get_all())
        app.make_page(page=app.page2)

        app.page2.listbox.selection_set(1)
        app.page2.remove()
        
        root.destroy()
        assert len(testedDB.Gains.get_all()) == 2 and len(testedDB.Gains.get_all_filter(['2', 30, self.curr_date])) == 0


    def testGUIDisplayCategoryRemove(self):
        testedDB.Categories.add('1')
        testedDB.Categories.add('2')

        root = Tk()
        app = testedGUI.App(root)
        app.page3.fill(testedDB.Categories.get_all())
        app.make_page(page=app.page3)

        app.page3.listbox.selection_set(0)
        app.page3.remove()

        guiDisplay = app.page3.listbox.get(0, END)
        root.destroy()

        assert len(guiDisplay) == 1 and guiDisplay[0] == '2'

    
    def testGUIDisplayGainsRemove(self):
        itemToAdd1 = ['item1', 100, self.curr_date]
        itemToAdd2 = ['item2', 100, self.curr_date]
        itemToAdd3 = ['item3', 100, self.curr_date]
        testedDB.Gains.add(itemToAdd1, self.curr_date)
        testedDB.Gains.add(itemToAdd2, self.curr_date)
        testedDB.Gains.add(itemToAdd3, self.curr_date)

        root = Tk()
        app = testedGUI.App(root)
        app.page2.fill(testedDB.Gains.get_all())
        app.make_page(page=app.page2)

        app.page2.listbox.selection_set(1)
        app.page2.remove()

        guiDisplay = list(app.page2.listbox.get(0, END))
        root.destroy()
        
        items = []
        for x in guiDisplay:
            id, name, price, date = x.split(' ')
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            listedItem = [name, float(price), date]
            items.append(listedItem)

        assert items == [itemToAdd1, itemToAdd3]

    def testGUIDisplaySpendingsRemove(self):
        testedDB.Categories.add('a')
        testedDB.Gains.add(['item1', 1000, self.curr_date], self.curr_date)
        itemToAdd1 = ['item1', 'a', 100, self.curr_date]
        itemToAdd2 = ['item2', 'a', 100, self.curr_date]
        itemToAdd3 = ['item3', 'a', 100, self.curr_date]
        testedDB.Spendings.add(itemToAdd1, self.curr_date)
        testedDB.Spendings.add(itemToAdd2, self.curr_date)
        testedDB.Spendings.add(itemToAdd3, self.curr_date)

        root = Tk()
        app = testedGUI.App(root)
        app.page1.fill(testedDB.Spendings.get_all())
        app.make_page(page=app.page1)

        app.page1.listbox.selection_set(1)
        app.page1.remove()
        
        guiDisplay = list(app.page1.listbox.get(0, END))
        root.destroy()
        
        items = []
        for x in guiDisplay:
            id, name, category, price, date = x.split(' ')
            date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
            listedItem = [name, category, float(price), date]
            items.append(listedItem)

        assert items == [itemToAdd1, itemToAdd3]
        
if __name__ == '__main__':
    unittest.main()
