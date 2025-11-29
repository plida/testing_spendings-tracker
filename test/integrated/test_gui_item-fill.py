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
    yield datetime.date(2025, 11, 26)

@pytest.fixture()
def app():
    root = Tk()
    app = testedGUI.App(root)
    yield app
    root.destroy()

# in page's list item info is separated by whitespaces, difficult to test without stripping them beforehand
def stripWhitespace(item): 
    for x in item:
        if isinstance(x, str):
            x.strip()
    return item

def testGUIFillCategories(app):
    itemToAdd = 'item'

    testedDB.Categories.add(itemToAdd)

    app.make_page(page=app.page3)
    app.page3.fill(testedDB.Categories.get_all())
    guiDisplay = app.page3.listbox.get(0, END)
    
    listedItem = guiDisplay[0]

    assert listedItem == itemToAdd

def testGUIFillGains(app, curr_date):
    itemToAdd = stripWhitespace(['item', 500, curr_date])
    testedDB.Gains.add(itemToAdd)

    app.make_page(page=app.page2)
    app.page2.fill(testedDB.Gains.get_all())
    guiDisplay = list(app.page2.listbox.get(0, END))
    
    id, name, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()

    listedItem = [name, float(price), date]

    assert listedItem == itemToAdd

def testGUIFillSpendings(app, curr_date):
    testedDB.Categories.add('a')
    testedDB.Gains.add(['salary', 5000, curr_date])
    itemToAdd = stripWhitespace(['item', 'a', 100, curr_date])

    testedDB.Spendings.add(itemToAdd)

    app.make_page(page=app.page1)

    app.page1.fill(testedDB.Spendings.get_all())
    guiDisplay = list(app.page1.listbox.get(0, END))
    
    id, name, category, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    listedItem = [name, category, float(price), date]

    assert listedItem == itemToAdd
    