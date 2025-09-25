from src import db 
import datetime
import unittest

class testGetGains(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2025, 1, 21)
        db.initiate("test/test_spendings.db")
        self.clearData(db.Sessions())
        self.gains_list = [["1", 10000, datetime.date(2025, 1, 1)], 
                           ["2", 20000, datetime.date(2025, 1, 2)],
                           ["3", 30000, datetime.date(2025, 2, 1)],
                           ["4", 40000, datetime.date(2025, 2, 2)],
                           ["5", 50000, datetime.date(2024, 1, 1)],
                           ["6", 60000, datetime.date(2024, 2, 1)]]
        self.gains_removed = [2, 4]

        for gain in self.gains_list:
            db.Gains.add(gain, self.curr_date)
        for gain in self.gains_removed:
            db.Gains.remove(gain)

    def clearData(self, session):
        meta = db.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    #def test_getall(self):
        #data = db.Gains.get_all()
        #assert len(data) == len(self.gains_list) - len(self.gains_removed)

    

if __name__ == '__main__':
    unittest.main()