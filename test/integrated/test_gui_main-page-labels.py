from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *
from unittest.mock import Mock

import datetime
import unittest

class testCheckLabels(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2024, 11, 26)
        testedDB.initiate("test/integrated/spendings.db")
        self.clearData(testedDB.initSessions())

    def clearData(self, session):
        meta = testedDB.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def testGUITotal(self):
        testedDB.Categories.add("одежда")
        testedDB.Spendings.add(["шляпа", "одежда", 5000, self.curr_date])
        testedDB.Spendings.add(["куртка", "одежда", 2000, self.curr_date])
        testedDB.Gains.add(["шляпа", 30000, self.curr_date])

        root = Tk()
        app = testedGUI.App(root)

        app.totalVAR.set(testedGUIscript.calculate_total())   

        label_var = app.total_label.cget("textvariable")
        label_text = app.total_label.getvar(label_var)

        root.destroy()

        assert label_text == 30000 - (5000 + 2000)

    def testGUIGainsMonth(self):
        testedDB.Gains.add(["шляпа", 30000, datetime.date(2024, 10, 31)])
        testedDB.Gains.add(["шляпа", 1000, datetime.date(2024, 12, 1)])
        testedDB.Gains.add(["шляпа", 500, datetime.date(2024, 11, 1)])
        testedDB.Gains.add(["шляпа", 20, datetime.date(2024, 11, 24)])
        testedDB.Gains.add(["шляпа", 1, datetime.date(2024, 11, 30)])
        
        root = Tk()
        app = testedGUI.App(root)
        app.gainsVAR.set(testedGUIscript.calculate_month_gain(self.curr_date))  

        label_var = app.gain_label.cget("textvariable")
        label_text = app.gain_label.getvar(label_var)

        root.destroy()

        assert label_text == 500 + 20 + 1

    def testGUISpendingsMonth(self):
        testedDB.Categories.add("одежда")
        testedDB.Spendings.add(["шляпа", "одежда", 10000, datetime.date(2024, 11, 30)])
        testedDB.Spendings.add(["шляпа", "одежда", 7000, datetime.date(2024, 12, 1)])
        testedDB.Spendings.add(["шляпа", "одежда", 600, datetime.date(2024, 11, 1)])
        testedDB.Spendings.add(["шляпа", "одежда", 40, datetime.date(2024, 11, 24)])
        testedDB.Spendings.add(["шляпа", "одежда", 5, datetime.date(2024, 10, 31)])
        
        root = Tk()
        app = testedGUI.App(root)
        app.spendingsVAR.set(testedGUIscript.calculate_month_spend(self.curr_date))

        label_var = app.spend_label.cget("textvariable")
        label_text = app.spend_label.getvar(label_var)

        root.destroy()

        assert label_text == 10000 + 600 + 40

        
if __name__ == '__main__':
    unittest.main()
