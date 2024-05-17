import datetime

import db


def add_category(name):
    result = db.Categories.add(name)
    return result


def remove_category(name):
    db.Categories.remove(name)


def add_spending(data):
    result = db.Spendings.add(data)
    calculate_total()
    calculate_month_spend()
    return result


def remove_spending(uid):
    db.Spendings.remove(uid)
    calculate_total()
    calculate_month_spend()


def add_gain(data):
    result = db.Gains.add(data)
    calculate_month_gain()
    return result


def remove_gain(uid):
    db.Gains.remove(uid)
    calculate_month_gain()


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
        sm += row[2]
    return sm


def sort_data(data, ind):
    try:
        sorted(data, key=lambda student: student[ind])
        return data
    except ...:
        return False