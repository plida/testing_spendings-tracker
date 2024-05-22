import db


def add_category(name):
    result = db.Categories.add(name)
    return result


def remove_category(name):
    db.Categories.remove(name)


def add_spending(data, totalvar):
    if not data or data[0] == "" and data[1] == "" and data[2] == "" and not data[3]:
        return "EXIT"
    try:
        cost = float(data[2])
        if cost <= totalvar.get():
            result = db.Spendings.add(data)
            calculate_total()
            calculate_month_spend()
        else:
            result = "ERR_nomoney"
    except ValueError or TypeError:
        result = "ERR_value"
    return result


def remove_spending(uid):
    db.Spendings.remove(uid)
    calculate_total()
    calculate_month_spend()


def add_gain(data):
    result = db.Gains.add(data)
    calculate_total()
    calculate_month_gain()
    return result


def remove_gain(uid):
    db.Gains.remove(uid)
    calculate_total()
    calculate_month_gain()


def calculate_total():
    data1 = db.Spendings.get_all()
    data2 = db.Gains.get_all()
    sm = 0
    for row in data1:
        sm -= row[3]
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


def sort(data, ind):
    try:
        data = sorted(data, key=lambda line: line[ind])
        return data
    except TypeError:
        return False
