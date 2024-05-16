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
        _session.commit()
        return data

    @staticmethod
    def get_all_filter(data):
        _session = Sessions()
        new_data = []
        if data == "":
            new_data = Categories.get_all()
            return new_data

        for category in _session.query(Categories):
            if category.name.find(data) != -1 and category.used != 0:
                new_data.append(category.name)
        _session.commit()
        return new_data


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
            if data[0] == "" or data[1] == "" or data[2] == "" or not data[3]:
                return
            try:
                data[2] = float(data[2])
                if data[2] > 0:
                    _session = Sessions()
                    query = Spendings(name=data[0].lower(), category=data[1].lower(), cost=data[2], date=data[3],
                                      refunded=0)
                    _session.add(query)
                    _session.commit()
            except ValueError:
                print("err")
        except TypeError or IndexError or sqlalchemy.exc.StatementError as error:
            print("Ошибка при добавлении траты:", error)

    @staticmethod
    def remove(uid):
        _session = Sessions()
        _session.query(Spendings).filter(Spendings.id == uid).update({"refunded": 1})
        _session.commit()

    @staticmethod
    def get_all():
        _session = Sessions()
        data = []
        for spending in _session.query(Spendings).filter_by(refunded=False):
            data.append((spending.id, spending.name, spending.category, spending.cost, spending.date))
        _session.commit()
        return data

    @staticmethod
    def get_all_filter(data):
        _session = Sessions()
        new_data = []
        if data[0] == "" and not data[1] and not data[2] and not data[3]:
            new_data = Spendings.get_all()
            return new_data
        if not data[1]:
            data[1] = ""
        if not data[2]:
            data[2] = 0
        if not data[3]:
            data[3] = ""
        for spending in _session.query(Spendings):
            if ((spending.name.find(data[0]) != -1 or data[0] == "") and (
                    spending.category == data[1] or data[1] == "") and (spending.cost == data[2] or data[2] == 0)
                    and (spending.date == data[3] or data[3] == "") and (spending.refunded == False)):
                new_data.append((spending.id, spending.name, spending.category, spending.cost, spending.date))
        _session.commit()
        return new_data

    @staticmethod
    def get_all_recent():
        _session = Sessions()
        data = []
        for spending in _session.query(Spendings):
            if spending.date > datetime.date.today() - datetime.timedelta(days=30) and spending.refunded == 0:
                data.append((spending.id, spending.name, spending.category, spending.cost, spending.date))
        _session.commit()
        return data


class Gains(Base):
    __tablename__ = 'gains'
    id: Mapped[int] = db.Column(db.Integer, primary_key=True)
    name: Mapped[str] = db.Column(db.String(20), nullable=False)
    money: Mapped[float]
    date: Mapped[datetime.date]
    deleted: Mapped[bool]

    @staticmethod
    def add(data):
        try:
            if data[0] == "" or data[1] == "" or not data[2]:
                return
            try:
                data[1] = float(data[1])
                if data[1] > 0:
                    _session = Sessions()
                    query = Gains(name=data[0].lower(), money=data[1], date=data[2],
                                  deleted=0)
                    _session.add(query)
                    _session.commit()
            except ValueError:
                print("err")
        except TypeError or IndexError or ValueError or sqlalchemy.exc.StatementError as error:
            print("Ошибка при добавлении прибыли:", error)

    @staticmethod
    def remove(uid):
        _session = Sessions()
        _session.query(Gains).filter(Gains.id == uid).update({"deleted": 1})
        _session.commit()

    @staticmethod
    def get_all():
        _session = Sessions()
        data = []
        for gain in _session.query(Gains).filter_by(deleted=False):
            data.append((gain.id, gain.name, gain.money, gain.date))
        _session.commit()
        return data

    @staticmethod
    def get_all_filter(data):
        _session = Sessions()
        new_data = []
        if data[0] == "" and not data[1] and not data[2]:
            new_data = Gains.get_all()
            return new_data
        if not data[1]:
            data[1] = 0
        if not data[2]:
            data[2] = ""
        for gain in _session.query(Gains):
            if ((gain.name.find(data[0]) != -1 or data[0] == "") and (gain.money == data[1] or data[1] == 0)
                    and (gain.date == data[2] or data[2] == "") and (gain.deleted == False)):
                new_data.append((gain.id, gain.name, gain.money, gain.date))
        _session.commit()
        return new_data

    @staticmethod
    def get_all_recent():
        _session = Sessions()
        data = []
        for gain in _session.query(Gains):
            if gain.date > datetime.date.today() - datetime.timedelta(days=30) and gain.deleted == 0:
                data.append((gain.id, gain.name, gain.money, gain.date))
        _session.commit()
        return data


engine = db.create_engine("sqlite:///spendings.db", echo=True)
Base.metadata.create_all(engine)
Sessions = sessionmaker(bind=engine)
