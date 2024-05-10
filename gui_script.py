import db


def add_category(name):
    if name:
        db.Categories.add(name)


def remove_category(name):
    db.Categories.remove(name)


def add_spending(data):
    db.Spendings.add(data)

def remove_spending(uid):
    db.Spendings.remove(uid)
