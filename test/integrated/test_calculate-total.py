from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
import pytest
import datetime

def clearData(session):
    meta = testedDB.Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

@pytest.fixture(autouse=True)
def initDB():
    testedDB.initiate("test/integrated/spendings.db")
    clearData(testedDB.initSessions())
    yield
    clearData(testedDB.initSessions())

@pytest.fixture()
def curr_date():
    yield datetime.date(2024, 11, 26)


def testCalculateTotal(curr_date):
    testedDB.Categories.add("одежда")
    testedDB.Spendings.add(["шляпа", "одежда", 5000, curr_date])
    testedDB.Spendings.add(["куртка", "одежда", 2000, curr_date])
    testedDB.Gains.add(["зарплата", 30000, curr_date])
    total = testedGUIscript.calculate_total()
    assert total == 30000 - (5000 + 2000)

def testCalculateMonthGains(curr_date):
    testedDB.Gains.add(["шляпа", 30000, datetime.date(2024, 10, 31)])
    testedDB.Gains.add(["шляпа", 1000, datetime.date(2024, 12, 1)])
    testedDB.Gains.add(["шляпа", 500, datetime.date(2024, 11, 1)])
    testedDB.Gains.add(["шляпа", 20, datetime.date(2024, 11, 24)])
    testedDB.Gains.add(["шляпа", 1, datetime.date(2024, 11, 30)])
    total = testedGUIscript.calculate_month_gain(curr_date)
    assert total == 500 + 20 + 1

def testCalculateMonthSpendings(curr_date):
    testedDB.Categories.add("одежда")
    testedDB.Spendings.add(["шляпа", "одежда", 10000, datetime.date(2024, 11, 30)])
    testedDB.Spendings.add(["шляпа", "одежда", 7000, datetime.date(2024, 12, 1)])
    testedDB.Spendings.add(["шляпа", "одежда", 600, datetime.date(2024, 11, 1)])
    testedDB.Spendings.add(["шляпа", "одежда", 40, datetime.date(2024, 11, 24)])
    testedDB.Spendings.add(["шляпа", "одежда", 5, datetime.date(2024, 10, 31)])
    total = testedGUIscript.calculate_month_spend(curr_date)
    assert total == 10000 + 600 + 40
