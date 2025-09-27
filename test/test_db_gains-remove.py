from src import db as testedDB 
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

class testRemoveGains(unittest.TestCase):
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

    def addItem(self, data):
        _session = self.Sessions()
        query = Gains(name=data[0].lower(), money=data[1], date=data[2],
                    deleted=0)
        _session.add(query)
        _session.commit()

    def listItems(self):
        _session = self.Sessions()
        data = []
        for gain in _session.query(Gains).filter_by(deleted=False):
            data.append((gain.id, gain.name, gain.money, gain.date))
        _session.commit()
        return data

    def test_removeGains(self):
        self.addItem(["зарплата", 50000, self.curr_date])
        self.addItem(["подарок", 5000, self.curr_date])
        testedDB.Gains.remove(1, self.Sessions)
        assert self.listItems()[0][1] == "подарок"

    def test_removeNonExistentGains(self):
        self.addItem(["зарплата", 50000, self.curr_date])
        self.addItem(["подарок", 5000, self.curr_date])
        testedDB.Gains.remove(4, self.Sessions)
        assert self.listItems()[1][1] == "подарок"    

if __name__ == '__main__':
    unittest.main()

    