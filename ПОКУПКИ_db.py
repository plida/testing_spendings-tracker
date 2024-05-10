import datetime
import sqlalchemy as db
import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class Categories(Base):
    __tablename__ = 'categories'

    name: Mapped[str] = db.Column(db.String, primary_key=True)
    used: Mapped[bool]

    @staticmethod
    def add(name):
        try:
            name = name.lower()
            _session = Sessions()
            x = _session.query(Categories).filter_by(name=name)
            exists = x.first()
            if exists:
                print(f"Категория {name} уже существует.")
                x.update({"used": 1})
                _session.commit()
                return
            query = Categories(name=name, used=True)
            _session.add(query)
            _session.commit()
        except TypeError or sqlalchemy.exc.StatementError as error:
            print("Ошибка при добавлении категории:", error)

    @staticmethod
    def remove(name):
        try:
            name = name.lower()
            _session = Sessions()
            x = _session.query(Categories).filter_by(name=name)
            exists = x.first()
            x.update({"used": 0})
            _session.commit()

        except TypeError or sqlalchemy.exc.StatementError as error:
            print("Ошибка при удалении категории:", error)

    @staticmethod
    def get_all():
        _session = Sessions()
        data = []
        for category in _session.query(Categories).filter_by(used=True):
            data.append(category.name)
        return data


class Spendings(Base):
    __tablename__ = 'spendings'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str]
    category: Mapped[str]
    cost: Mapped[float]
    date: Mapped[datetime.date]
    refunded: Mapped[bool]

    @staticmethod
    def add(data):
        try:
            _session = Sessions()
            print(data, len(data))
            data[2] = float(data[2])
            if data[2] > 0:
                query = Spendings(name=data[0], category=data[1], cost=data[2], date=data[3], refunded=0)
                _session.add(query)
                _session.commit()
        except TypeError or IndexError or sqlalchemy.exc.StatementError as error:
            print("Ошибка при добавлении траты:", error)

    @staticmethod
    def remove(uid):
        _session = Sessions()
        _session.query(Spendings).filter(Spendings.id == uid).delete()
        _session.commit()

    @staticmethod
    def get_all():
        _session = Sessions()
        data = []
        for spending in _session.query(Spendings):
            data.append((spending.id, spending.name, spending.category, spending.cost, spending.date))
        return data


engine = db.create_engine("sqlite:///spendings.db", echo=True)
Base.metadata.create_all(engine)
Sessions = sessionmaker(bind=engine)