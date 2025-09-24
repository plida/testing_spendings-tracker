from src import db 
import datetime
import unittest

class testAddGains(unittest.TestCase):
    def setUp(self):
        self.curr_date = datetime.date(2025, 9, 21)
        db.initiate("test/test_spendings.db")

    def clearData(self, session):
        meta = db.Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def test_removeGains(self):
        self.clearData(db.Sessions())
        db.Gains.add(["зарплата", 50000, self.curr_date], self.curr_date)
        db.Gains.add(["подарок", 5000, self.curr_date], self.curr_date)
        db.Gains.remove(1)
        assert db.Gains.get_all()[0][1] == "подарок" 

if __name__ == '__main__':
    unittest.main()

    