from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *
from unittest.mock import Mock

import datetime
import unittest

class testCalculateTotal(unittest.TestCase):
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
        app.page1.fill(testedDB.Spendings.get_all())
        app.page2.fill(testedDB.Gains.get_all())
        app.page3.fill(testedDB.Categories.get_all())
        app.make_page(page=app.page3)

        app.page3.listbox.selection_set(1)
        app.page3.remove()

        assert len(testedDB.Categories.get_all()) == 2 and len(testedDB.Categories.get_all_filter('2')) == 0
        
if __name__ == '__main__':
    unittest.main()
