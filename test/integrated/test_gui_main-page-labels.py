from src.app import gui as testedGUI
from src.app import db as testedDB
from src.app import gui_script as testedGUIscript
from tkinter import *
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

@pytest.fixture()
def app():
    root = Tk()
    app = testedGUI.App(root)
    yield app
    root.destroy()

def testGUITotal(app, curr_date):
    testedDB.Categories.add("одежда")
    testedDB.Spendings.add(["шляпа", "одежда", 5000, curr_date])
    testedDB.Spendings.add(["куртка", "одежда", 2000, curr_date])
    testedDB.Gains.add(["шляпа", 30000, curr_date])

    app.totalVAR.set(testedGUIscript.calculate_total())   

    label_var = app.total_label.cget("textvariable")
    label_text = app.total_label.getvar(label_var)

    assert label_text == 30000 - (5000 + 2000)

def testGUIGainsMonth(app, curr_date):
    testedDB.Gains.add(["шляпа", 30000, datetime.date(2024, 10, 31)])
    testedDB.Gains.add(["шляпа", 1000, datetime.date(2024, 12, 1)])
    testedDB.Gains.add(["шляпа", 500, datetime.date(2024, 11, 1)])
    testedDB.Gains.add(["шляпа", 20, datetime.date(2024, 11, 24)])
    testedDB.Gains.add(["шляпа", 1, datetime.date(2024, 11, 30)])
    
    app.gainsVAR.set(testedGUIscript.calculate_month_gain(curr_date))  

    label_var = app.gain_label.cget("textvariable")
    label_text = app.gain_label.getvar(label_var)

    assert label_text == 500 + 20 + 1

def testGUISpendingsMonth(app, curr_date):
    testedDB.Categories.add("одежда")
    testedDB.Spendings.add(["шляпа", "одежда", 10000, datetime.date(2024, 11, 30)])
    testedDB.Spendings.add(["шляпа", "одежда", 7000, datetime.date(2024, 12, 1)])
    testedDB.Spendings.add(["шляпа", "одежда", 600, datetime.date(2024, 11, 1)])
    testedDB.Spendings.add(["шляпа", "одежда", 40, datetime.date(2024, 11, 24)])
    testedDB.Spendings.add(["шляпа", "одежда", 5, datetime.date(2024, 10, 31)])
    
    app.spendingsVAR.set(testedGUIscript.calculate_month_spend(curr_date))

    label_var = app.spend_label.cget("textvariable")
    label_text = app.spend_label.getvar(label_var)

    assert label_text == 10000 + 600 + 40
