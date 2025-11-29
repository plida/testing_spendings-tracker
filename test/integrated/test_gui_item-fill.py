from src.app import db as testDB
from tkinter import END
import datetime

# in page's list item info is separated by whitespaces, difficult to test without stripping them beforehand
def stripWhitespace(item): 
    for x in item:
        if isinstance(x, str):
            x.strip()
    return item

def testGUIFillCategories(app):
    itemToAdd = 'item'
    testDB.Categories.add(itemToAdd)
    app.make_page(page=app.page3)

    app.page3.fill(testDB.Categories.get_all())

    guiDisplay = app.page3.listbox.get(0, END)
    listedItem = guiDisplay[0]

    assert listedItem == itemToAdd

def testGUIFillGains(app, curr_date):
    itemToAdd = stripWhitespace(['item', 500, curr_date])
    testDB.Gains.add(itemToAdd)
    app.make_page(page=app.page2)

    app.page2.fill(testDB.Gains.get_all())

    guiDisplay = list(app.page2.listbox.get(0, END))
    id, name, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    listedItem = [name, float(price), date]

    assert listedItem == itemToAdd

def testGUIFillSpendings(app, curr_date):
    testDB.Categories.add('a')
    testDB.Gains.add(['salary', 5000, curr_date])
    itemToAdd = stripWhitespace(['item', 'a', 100, curr_date])
    testDB.Spendings.add(itemToAdd)
    app.make_page(page=app.page1)

    app.page1.fill(testDB.Spendings.get_all())

    guiDisplay = list(app.page1.listbox.get(0, END))
    id, name, category, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    listedItem = [name, category, float(price), date]

    assert listedItem == itemToAdd
    