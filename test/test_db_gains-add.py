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

    def test_addGains(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", 50000, self.curr_date], self.curr_date)
        assert res == True

    def test_longname(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата01234567890", 50000, self.curr_date], self.curr_date)
        assert res=="ERR_toolong"

    def test_emptyname(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["", 50000, self.curr_date], self.curr_date)
        assert res=="ERR_empty"

    def test_emptysum(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", "", self.curr_date], self.curr_date)
        assert res=="ERR_empty"

    def test_emptydate(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", 50000, ""], self.curr_date)
        assert res=="ERR_empty"

    def test_largesum(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", 10**20, self.curr_date], self.curr_date)
        assert res=="ERR_value"

    def test_wrongsum(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", "10**20", self.curr_date], self.curr_date)
        assert res=="ERR_value"

    def test_futuredate(self):
        self.clearData(db.Sessions())
        res = db.Gains.add(["зарплата", 50000, datetime.date(9999, 9, 21)], self.curr_date)
        assert res=="ERR_future"

if __name__ == '__main__':
    unittest.main()