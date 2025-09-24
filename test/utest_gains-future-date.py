from src import db 
import datetime
import os

os.remove("test/test_spendings.db")
db.initiate("test/test_spendings.db")
currentdate = datetime.date(2000, 2, 24)
db.Gains.add(["зарплата", 50000, datetime.date(2005, 2, 24)], currentdate)

def test_checkDate():
    assert (db.Gains.get_all())[0][3] == datetime.date(2005, 2, 24)