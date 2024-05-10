import ПОКУПКИ_db as Db


def add_category(name):
    if name:
        Db.Categories.add(name)


def remove_category(name):
    Db.Categories.remove(name)


def add_spending(data):
    Db.Spendings.add(data)

def remove_spending(uid):
    Db.Spendings.remove(uid)
