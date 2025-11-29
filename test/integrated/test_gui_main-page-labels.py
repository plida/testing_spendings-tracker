from src.app import db as testDB
from src.app import gui_script as testedGUIscript
from tkinter import END
import pytest
import datetime

@pytest.fixture()
def curr_date():
    yield datetime.date(2024, 11, 26)

def testGUITotal(app, curr_date):
    testDB.Categories.add("одежда")
    testDB.Spendings.add(["шляпа", "одежда", 5000, curr_date])
    testDB.Spendings.add(["куртка", "одежда", 2000, curr_date])
    testDB.Gains.add(["шляпа", 30000, curr_date])

    app.totalVAR.set(testedGUIscript.calculate_total())   

    label_var = app.total_label.cget("textvariable")
    label_text = app.total_label.getvar(label_var)

    assert label_text == 30000 - (5000 + 2000)

def testGUIGainsMonth(app, curr_date):
    testDB.Gains.add(["шляпа", 30000, datetime.date(2024, 10, 31)])
    testDB.Gains.add(["шляпа", 1000, datetime.date(2024, 12, 1)])
    testDB.Gains.add(["шляпа", 500, datetime.date(2024, 11, 1)])
    testDB.Gains.add(["шляпа", 20, datetime.date(2024, 11, 24)])
    testDB.Gains.add(["шляпа", 1, datetime.date(2024, 11, 30)])
    
    app.gainsVAR.set(testedGUIscript.calculate_month_gain(curr_date))  

    label_var = app.gain_label.cget("textvariable")
    label_text = app.gain_label.getvar(label_var)

    assert label_text == 500 + 20 + 1

def testGUISpendingsMonth(app, curr_date):
    testDB.Categories.add("одежда")
    testDB.Spendings.add(["шляпа", "одежда", 10000, datetime.date(2024, 11, 30)])
    testDB.Spendings.add(["шляпа", "одежда", 7000, datetime.date(2024, 12, 1)])
    testDB.Spendings.add(["шляпа", "одежда", 600, datetime.date(2024, 11, 1)])
    testDB.Spendings.add(["шляпа", "одежда", 40, datetime.date(2024, 11, 24)])
    testDB.Spendings.add(["шляпа", "одежда", 5, datetime.date(2024, 10, 31)])
    
    app.spendingsVAR.set(testedGUIscript.calculate_month_spend(curr_date))

    label_var = app.spend_label.cget("textvariable")
    label_text = app.spend_label.getvar(label_var)

    assert label_text == 10000 + 600 + 40
