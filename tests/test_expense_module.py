from modules.expense_module import *
import pytest
import sqlite3


@pytest.fixture()
def db():
    conn = sqlite3.connect("tests/test_database.db")
    return conn


def test_insert_expense(db):
    """
    Test if expenses can be added to database
    """
    assert insert_expense(db, 1, "Hot Dog", "2022-04-01", "Food", 1.50) == 5

    cur = db.cursor()
    cur.execute(
        "DELETE FROM expenses WHERE id=? AND user_id=?",
        (
            5,
            1,
        ),
    )
    db.commit()


def test_select_one_expense(db):
    assert select_one_expense(db, 1, 1) == (1, 1, "Coffee", "2022-04-29", "Food", 4.5)


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


def test_get_total_expenses(db):
    c = get_total_expenses(db, 1)
    assert c == 1217.25


def test_total_expenses_by_category(db):
    u1 = get_total_expenses_by_category(db, 1, "Food")
    u2 = get_total_expenses_by_category(db, 2, "Food")
    assert u1 == 4.5
    assert u2 == 10.95


def test_select_expenses_by_category(db):
    f = select_expenses_by_category(db, 1, "Technology")
    assert f == [(2, 1, "Laptop", "2022-04-01", "Technology", 1200)]


def test_get_all_expenses(db):
    p = get_all_expenses(db)
    assert p == [
        (1, 1, "Coffee", "2022-04-29", "Food", 4.5),
        (2, 1, "Laptop", "2022-04-01", "Technology", 1200),
        (3, 1, "Movie", "2022-03-29", "Entertainment", 12.75),
        (4, 2, "Burger", "2022-03-29", "Food", 10.95),
    ]


def test_update_expense(db):
    assert update_expense(db, 1, "Coffee", "Food", 4.5, "2022-04-29") == None


def test_get_user_categories(db):
    assert get_user_categories(db, 1) == ["Entertainment", "Food", "Technology"]


def test_get_expense_today(db):
    assert get_expense_today(db, 1) == get_expense_today(db, 1)


def test_get_expense_week(db):
    assert get_expense_week(db, 1) == get_expense_week(db, 1)


def test_get_expense_month(db):
    assert get_expense_month(db, 1) == get_expense_month(db, 1)


def test_get_expense_keyword(db):
    assert get_expense_keyword(db, 1, "Coffee") == (
        4.5,
        [(1, 1, "Coffee", "2022-04-29", "Food", 4.5)],
    )


def test_get_expense_category(db):
    assert get_expense_category(db, 1, "Food") == (
        4.5,
        [(1, 1, "Coffee", "2022-04-29", "Food", 4.5)],
    )


def test_get_expense_date_search(db):
    assert get_expense_date_search(db, 1, "2022-04-01") == [
        (2, 1, "Laptop", "2022-04-01", "Technology", 1200)
    ]
