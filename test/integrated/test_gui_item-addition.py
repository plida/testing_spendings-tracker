from src.app import db as testDB
from src.app import gui_script as testedGUIscript
from tkinter import END
import datetime

# in page's list item info is separated by whitespaces, difficult to test without stripping them beforehand
def stripWhitespace(item): 
    for x in item:
        if isinstance(x, str):
            x.strip()
    return item

def testGUIGainsAdd(app, curr_date):
    itemToAdd = ['item', 500, curr_date]
    app.make_page(page=app.page2)
    
    app.page2.add(itemToAdd)

    assert itemToAdd == list(testDB.Gains.get_all()[0][1:4])

def testGUISpendingsAdd(app, curr_date):
    testDB.Categories.add('a')
    testDB.Gains.add(['salary', 5000, curr_date])
    itemToAdd = stripWhitespace(['it em', 'a', 500, curr_date])
    app.make_page(page=app.page1)
    app.totalVAR.set(testedGUIscript.calculate_total())
    
    app.page1.add(itemToAdd)

    assert itemToAdd == list(testDB.Spendings.get_all()[0][1:5])

def testGUIDisplayCategoryAdd(app):
    itemToAdd = 'item'
    app.make_page(page=app.page3)

    app.page3.add(itemToAdd)

    guiDisplay = app.page3.listbox.get(0, END)
    listedItem = guiDisplay[0]

    assert listedItem == itemToAdd

def testGUIDisplayGainsAdd(app, curr_date):
    itemToAdd = stripWhitespace(['item', 500, curr_date])
    app.make_page(page=app.page2)

    app.page2.add(itemToAdd)

    guiDisplay = list(app.page2.listbox.get(0, END))
    id, name, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    listedItem = [name, float(price), date]

    assert listedItem == itemToAdd

def testGUIDisplaySpendingsAdd(app, curr_date):
    testDB.Categories.add('a')
    testDB.Gains.add(['salary', 5000, curr_date])
    itemToAdd = stripWhitespace(['item', 'a', 100, curr_date])
    app.make_page(page=app.page1)
    app.totalVAR.set(testedGUIscript.calculate_total())

    app.page1.add(itemToAdd)

    guiDisplay = list(app.page1.listbox.get(0, END))
    id, name, category, price, date = guiDisplay[0].split(' ')
    date = datetime.datetime.strptime(date, "%d/%m/%Y").date()
    listedItem = [name, category, float(price), date]

    assert listedItem == itemToAdd
