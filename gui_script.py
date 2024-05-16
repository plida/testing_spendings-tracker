import datetime

import db


def add_category(name):
    if name:
        db.Categories.add(name)


def remove_category(name):
    db.Categories.remove(name)


def add_spending(data):
    db.Spendings.add(data)
    calculate_total()


def remove_spending(uid):
    db.Spendings.remove(uid)
    calculate_total()


def add_gain(data):
    db.Gains.add(data)


def remove_gain(uid):
    db.Gains.remove(uid)


def calculate_total():
    data1 = db.Spendings.get_all()
    data2 = db.Gains.get_all()
    sm = 0
    for row in data1:
        sm += row[3]
    for row in data2:
        sm += row[2]
    return sm


def calculate_month_spend():
    data1 = db.Spendings.get_all_recent()
    sm = 0
    for row in data1:
        sm += row[3]
    return sm

def calculate_month_gain():
    data1 = db.Gains.get_all_recent()
    sm = 0
    for row in data1:
        sm += row[3]
    return sm