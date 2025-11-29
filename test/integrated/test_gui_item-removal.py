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

def testGUICategoryRemove(app):
    testedDB.Categories.add('1')
    testedDB.Categories.add('2')
    testedDB.Categories.add('3')

    app.page3.fill(testedDB.Categories.get_all())
    app.make_page(page=app.page3)

    app.page3.listbox.selection_set(1)
    app.page3.remove()

    assert len(testedDB.Categories.get_all()) == 2 and len(testedDB.Categories.get_all_filter('2')) == 0

def testGUISpendingsRemove(app, curr_date):
    testedDB.Categories.add('numbers')
    testedDB.Spendings.add(['1', 'numbers', 500, curr_date], curr_date)
    testedDB.Spendings.add(['2', 'numbers', 30, curr_date], curr_date)
    testedDB.Spendings.add(['3', 'numbers', 1, curr_date], curr_date)

    app.page1.fill(testedDB.Spendings.get_all())
    app.make_page(page=app.page1)

    app.page1.listbox.selection_set(1)
    app.page1.remove()
    
    assert len(testedDB.Spendings.get_all()) == 2 and len(testedDB.Spendings.get_all_filter(['2', 'numbers', 30, curr_date])) == 0

def testGUIGainsRemove(app, curr_date):
    testedDB.Gains.add(['1', 500, curr_date], curr_date)
    testedDB.Gains.add(['2', 30, curr_date], curr_date)
    testedDB.Gains.add(['3', 1, curr_date], curr_date)

    app.page2.fill(testedDB.Gains.get_all())
    app.make_page(page=app.page2)

    app.page2.listbox.selection_set(1)
    app.page2.remove()
    
    assert len(testedDB.Gains.get_all()) == 2 and len(testedDB.Gains.get_all_filter(['2', 30, curr_date])) == 0


def testGUIDisplayCategoryRemove(app):
    testedDB.Categories.add('1')
    testedDB.Categories.add('2')

    app.page3.fill(testedDB.Categories.get_all())
    app.make_page(page=app.page3)

    app.page3.listbox.selection_set(0)
    app.page3.remove()

    guiDisplay = app.page3.listbox.get(0, END)

    assert len(guiDisplay) == 1 and guiDisplay[0] == '2'


def testGUIDisplayGainsRemove(app, curr_date):
    itemToAdd1 = stripWhitespace(['item1', 100, curr_date])
    itemToAdd2 = stripWhitespace(['item2', 100, curr_date])
    itemToAdd3 = stripWhitespace(['item3', 100, curr_date])
    testedDB.Gains.add(itemToAdd1, curr_date)
    testedDB.Gains.add(itemToAdd2, curr_date)
    testedDB.Gains.add(itemToAdd3, curr_date)

    app.page2.fill(testedDB.Gains.get_all())
    app.make_page(page=app.page2)

    app.page2.listbox.selection_set(1)
    app.page2.remove()

    guiDisplay = list(app.page2.listbox.get(0, END))
    
    items = []
    for x in guiDisplay:
        id, name, price, date = x.split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        listedItem = [name, float(price), date]
        items.append(listedItem)

    assert items == [itemToAdd1, itemToAdd3]

def testGUIDisplaySpendingsRemove(app, curr_date):
    testedDB.Categories.add('a')
    testedDB.Gains.add(['item1', 1000, curr_date], curr_date)
    itemToAdd1 = stripWhitespace(['item1', 'a', 100, curr_date])
    itemToAdd2 = stripWhitespace(['item2', 'a', 100, curr_date])
    itemToAdd3 = stripWhitespace(['item3', 'a', 100, curr_date])
    testedDB.Spendings.add(itemToAdd1, curr_date)
    testedDB.Spendings.add(itemToAdd2, curr_date)
    testedDB.Spendings.add(itemToAdd3, curr_date)

    app.page1.fill(testedDB.Spendings.get_all())
    app.make_page(page=app.page1)

    app.page1.listbox.selection_set(1)
    app.page1.remove()

    guiDisplay = list(app.page1.listbox.get(0, END))
    
    items = []
    for x in guiDisplay:
        id, name, category, price, date = x.split(' ')
        date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
        listedItem = [name, category, float(price), date]
        items.append(listedItem)

    assert items == [itemToAdd1, itemToAdd3]
        