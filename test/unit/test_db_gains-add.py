from src.app import db as testedDB
import datetime
import unittest
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
class Base(DeclarativeBase):
    pass

class Gains(Base):
    __tablename__ = 'gains'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(20), nullable=False)
    money: Mapped[float]
    date: Mapped[datetime.date]
    deleted: Mapped[bool]

class testAddGains(unittest.TestCase):
    def initiateDB(self, path):
        global engine
        engine = db.create_engine("sqlite:///" + path, echo=True)
        Base.metadata.create_all(engine)
        self.Sessions = sessionmaker(bind=engine)

    def setUp(self):
        self.curr_date = datetime.date(2025, 9, 21)
        self.initiateDB("test/test_spendings.db")
        self.clearData(self.Sessions())

    def clearData(self, session):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            session.execute(table.delete())
        session.commit()

    def listItems(self):
        _session = self.Sessions()
        data = []
        for gain in _session.query(Gains).filter_by(deleted=False):
            data.append((gain.id, gain.name, gain.money, gain.date))
        _session.commit()
        return data

    def test_addGains(self):
        testedDB.Gains.add(["зарплата", 50000, self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 1

    def test_longname(self):
        testedDB.Gains.add(["зарплата01234567890", 50000, self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_emptyname(self):
        testedDB.Gains.add(["   ", 50000, self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_emptysum(self):
        testedDB.Gains.add(["зарплата", "   ", self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_emptydate(self):
        testedDB.Gains.add(["зарплата", 50000, "   "], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_largesum(self):
        testedDB.Gains.add(["зарплата", 10**20, self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_wrongsum(self):
        testedDB.Gains.add(["зарплата", "10**20", self.curr_date], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

    def test_futuredate(self):
        testedDB.Gains.add(["зарплата", 50000, datetime.date(9999, 9, 21)], self.curr_date, self.Sessions)
        assert len(self.listItems()) == 0

if __name__ == '__main__':
    unittest.main()