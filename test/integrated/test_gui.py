from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *

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

    def testCalculateTotal(self):
        root = Tk()
        app = testedGUI.App(root)
        app.page1.fill(testedDB.Spendings.get_all())
        app.page2.fill(testedDB.Gains.get_all())
        app.page3.fill(testedDB.Categories.get_all())

        app.page3._dialogue.e1 = 'alala'
        app.page3._dialogue.apply
        app.page3.add()

        assert len(testedDB.Categories.get_all_filter('alala')) == 1
        
if __name__ == '__main__':
    unittest.main()
