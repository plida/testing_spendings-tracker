from src.app import db as testedDB
import datetime
import unittest
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped
class Base(DeclarativeBase):
    pass

class Categories(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = db.Column(db.String(), primary_key=True)
    deleted: Mapped[bool]

class Spendings(Base):
    __tablename__ = 'spendings'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str]
    category: Mapped[str] = db.Column(db.String, db.ForeignKey(Categories.name))
    cost: Mapped[float]
    date: Mapped[datetime.date]
    deleted: Mapped[bool]

class testAddSpendings(unittest.TestCase):
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
        for spending in _session.query(Spendings).filter_by(deleted=False):
            data.append((spending.id, spending.name, spending.category, spending.cost, spending.date))
        _session.commit()
        return data
    
    def addCategory(self, data):
        _session = self.Sessions()
        query = Categories(name=data, deleted=0)
        _session.add(query)
        _session.commit()

    def addItem(self, data):
        _session = self.Sessions()
        query = Spendings(name=data[0].lower(), category=data[1], cost=data[2], date=data[3],
                    deleted=0)
        _session.add(query)
        _session.commit()

    def test_removeSpending(self):
        self.addCategory("одежда")
        self.addItem(["шляпа", "одежда", 5000, self.curr_date])
        self.addItem(["куртка", "одежда", 5000, self.curr_date])
        testedDB.Spendings.remove(1, self.Sessions)
        assert self.listItems()[0][1] == "куртка"
        

if __name__ == '__main__':
    unittest.main()