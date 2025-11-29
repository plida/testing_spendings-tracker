from src.app import gui as testedGUI
from src.app import db as testDB
from tkinter import *
import pytest
import datetime

def clearData(session):
    meta = testDB.Base.metadata
    for table in reversed(meta.sorted_tables):
        session.execute(table.delete())
    session.commit()

@pytest.fixture(autouse=True)
def initDB():
    testDB.initiate("test/integrated/spendings.db")
    clearData(testDB.initSessions())
    yield
    clearData(testDB.initSessions())

@pytest.fixture()
def curr_date():
    yield datetime.date(2025, 11, 26)

@pytest.fixture()
def app():
    root = Tk()
    app = testedGUI.App(root)
    yield app
    root.destroy()
