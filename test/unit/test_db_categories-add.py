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

class testAddCategories(unittest.TestCase):
    def initiateDB(self, path):
        global engine
        engine = db.create_engine("sqlite:///" + path, echo=True)
        Base.metadata.create_all(engine)
        self.Sessions = sessionmaker(bind=engine)

    def setUp(self):
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
        for category in _session.query(Categories).filter_by(deleted=False):
            data.append((category.name))
        _session.commit()
        return data

    def test_addGains(self):
        testedDB.Categories.add("одежда", self.Sessions)
        assert len(self.listItems()) == 1

    def test_duplicate(self):
        testedDB.Categories.add("одежда", self.Sessions)
        testedDB.Categories.add("одежда", self.Sessions)
        assert len(self.listItems()) == 1

    def test_duplicateUppercase(self):
        testedDB.Categories.add("одежда", self.Sessions)
        testedDB.Categories.add("Одежда", self.Sessions)
        assert len(self.listItems()) == 1

    def test_emptyname(self):
        testedDB.Categories.add("   ", self.Sessions)
        assert len(self.listItems()) == 0

if __name__ == '__main__':
    unittest.main()