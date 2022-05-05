from modules.expense_module import *
import pytest
import sql_db


@pytest.fixture
def db():
    conn = sql_db.create_connection('./database.db')
    return conn


def test_delete_one_expense(db):
    d = delete_one_expense(db, 1, 1,)
    pass


def test_get_total_expenses(db):
    c = get_total_expenses(db, 1)
    assert c == 1217.25


def test_total_expenses_by_category(db):
    u1 = get_total_expenses_by_category(db, 1, 'Food')
    u2 = get_total_expenses_by_category(db, 2, 'Food')
    assert u1 == 4.5
    assert u2 == 10.95


def test_select_expenses_by_category(db):
    f = select_expenses_by_category(db, 1, 'Technology')
    assert f == [(2, 1, 'Laptop', '2022-04-01', 'Technology', 1200)]


def test_get_all_expenses(db):
    p = get_all_expenses(db)
    assert p == [(1, 1, 'Coffee', '2022-04-29', 'Food', 4.5), (2, 1, 'Laptop', '2022-04-01', 'Technology', 1200),
                 (3, 1, 'Movie', '2022-03-29', 'Entertainment', 12.75), (4, 2, 'Burger', '2022-03-29', 'Food', 10.95)]
