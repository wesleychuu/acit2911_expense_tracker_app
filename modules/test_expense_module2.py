import pytest
import sqlite3

from expense_module import *


@pytest.fixture()
def db():
    conn = sqlite3.connect("database.db")
    return conn


def test_insert_expense(db):
    """
    Test if expenses can be added to database
    """
    assert insert_expense(db, 1, "Hot Dog", "2022-04-01", "Food", 1.50) == 5


def test_select_one_expense(db):
    assert select_one_expense(db, 5, 1) == (5, 1, "Hot Dog", "2022-04-01", "Food", 1.5)


def test_select_expenses_by_uid(db):
    assert select_expenses_by_uid(db, 2) == [
        (
            4,
            2,
            "Burger",
            "2022-03-29",
            "Food",
            10.95,
        )
    ]


# def test_delete_one_expense(db):
#     cur = db.cursor()
#     delete_one_expense(db, 5, 1)
#     cur.execute("SELECT length(* FROM expenses WHERE user_id=?)", (1,))
