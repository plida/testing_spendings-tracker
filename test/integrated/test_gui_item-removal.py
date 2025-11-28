from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *

import datetime
import unittest

class testRemove(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2025, 11, 26)
        testedDB.initiate("test/integrated/spendings.db")
        self.clearData(testedDB.initSessions())

    def clearData(self, session):
        meta = testedDB.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()
    
    """
    def testGUICategoryAdd(self):
        root = Tk()
        app = testedGUI.App(root)
        app.make_page(page=app.page3)
        dialogue = app.page3._dialogue(app.page3.master)
        dialogue.e1.insert(0, 'aaa')
        root.destroy()

        assert 1 == 0"""

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
        
if __name__ == '__main__':
    unittest.main()
