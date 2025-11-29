from src.app import db as testDB
from tkinter import END
import datetime

# in page's list item info is separated by whitespaces, difficult to test without stripping them beforehand
def stripWhitespace(item): 
    for x in item:
        if isinstance(x, str):
            x.strip()
    return item

def testGUICategoryRemove(app):
    testDB.Categories.add('1')
    testDB.Categories.add('2')
    testDB.Categories.add('3')
    app.page3.fill(testDB.Categories.get_all())
    app.make_page(page=app.page3)

    app.page3.listbox.selection_set(1)
    app.page3.remove()

    assert len(testDB.Categories.get_all()) == 2 and len(testDB.Categories.get_all_filter('2')) == 0

def testGUISpendingsRemove(app, curr_date):
    testDB.Categories.add('numbers')
    testDB.Spendings.add(['1', 'numbers', 500, curr_date], curr_date)
    testDB.Spendings.add(['2', 'numbers', 30, curr_date], curr_date)
    testDB.Spendings.add(['3', 'numbers', 1, curr_date], curr_date)
    app.page1.fill(testDB.Spendings.get_all())
    app.make_page(page=app.page1)

    app.page1.listbox.selection_set(1)
    app.page1.remove()
    
    assert len(testDB.Spendings.get_all()) == 2 and len(testDB.Spendings.get_all_filter(['2', 'numbers', 30, curr_date])) == 0

def testGUIGainsRemove(app, curr_date):
    testDB.Gains.add(['1', 500, curr_date], curr_date)
    testDB.Gains.add(['2', 30, curr_date], curr_date)
    testDB.Gains.add(['3', 1, curr_date], curr_date)
    app.page2.fill(testDB.Gains.get_all())
    app.make_page(page=app.page2)

    app.page2.listbox.selection_set(1)
    app.page2.remove()
    
    assert len(testDB.Gains.get_all()) == 2 and len(testDB.Gains.get_all_filter(['2', 30, curr_date])) == 0

def testGUIDisplayCategoryRemove(app):
    testDB.Categories.add('1')
    testDB.Categories.add('2')
    app.page3.fill(testDB.Categories.get_all())
    app.make_page(page=app.page3)

    app.page3.listbox.selection_set(0)
    app.page3.remove()

    guiDisplay = app.page3.listbox.get(0, END)

    assert len(guiDisplay) == 1 and guiDisplay[0] == '2'


def testGUIDisplayGainsRemove(app, curr_date):
    itemToAdd1 = stripWhitespace(['item1', 100, curr_date])
    itemToAdd2 = stripWhitespace(['item2', 100, curr_date])
    itemToAdd3 = stripWhitespace(['item3', 100, curr_date])
    testDB.Gains.add(itemToAdd1, curr_date)
    testDB.Gains.add(itemToAdd2, curr_date)
    testDB.Gains.add(itemToAdd3, curr_date)
    app.page2.fill(testDB.Gains.get_all())
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
    testDB.Categories.add('a')
    testDB.Gains.add(['item1', 1000, curr_date], curr_date)
    itemToAdd1 = stripWhitespace(['item1', 'a', 100, curr_date])
    itemToAdd2 = stripWhitespace(['item2', 'a', 100, curr_date])
    itemToAdd3 = stripWhitespace(['item3', 'a', 100, curr_date])
    testDB.Spendings.add(itemToAdd1, curr_date)
    testDB.Spendings.add(itemToAdd2, curr_date)
    testDB.Spendings.add(itemToAdd3, curr_date)
    app.page1.fill(testDB.Spendings.get_all())
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
        