from tkinter import *
from . import gui
from . import db

root = Tk()
app = gui.App(root)
db.initiate("src/app/spendings.db")
app.page1.fill(db.Spendings.get_all())
app.page2.fill(db.Gains.get_all())
app.page3.fill(db.Categories.get_all())

sm1 = sm2 = 0
data1, data2 = db.Spendings.get_all(), db.Gains.get_all()
for row in data1:
    sm1 += row[3]
for row in data2:
    sm2 += row[2]
app.totalVAR.set(sm2-sm1)

sm1 = sm2 = 0
data1, data2 = db.Spendings.get_all_recent(), db.Gains.get_all_recent()
for row in data1:
    sm1 += row[3]
for row in data2:
    sm2 += row[2]
app.spendingsVAR.set(sm1)
app.gainsVAR.set(sm2)

root.mainloop()
