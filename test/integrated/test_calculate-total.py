from src.app import db as testedDB
from src.app import gui_script as testedGUIscript

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
        testedDB.Categories.add("одежда")
        testedDB.Spendings.add(["шляпа", "одежда", 5000, self.curr_date])
        testedDB.Spendings.add(["куртка", "одежда", 2000, self.curr_date])
        testedDB.Gains.add(["зарплата", 30000, self.curr_date])
        total = testedGUIscript.calculate_total()
        assert total == 30000 - (5000 + 2000)
        
if __name__ == '__main__':
    unittest.main()
