import sqlite3


def insert_expense(
    conn, uid: int, name: str, date: str, category: str, amount: int
) -> int:
    """
    Insert a new expense into expenses table

    Parameters:
        conn:               the Connection obj
        uid (int):          user id
        name (str):         title of expense
        date (str):         date of expense
        category (str):     type of expense
        amount (int):       amount of expense

    Return:
        id of last row
    """
    sql = """ INSERT INTO expenses(user_id,name,date,category,amount) VALUES(?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(
        sql,
        (
            uid,
            name,
            date,
            category,
            amount,
        ),
    )
    conn.commit()

    return cur.lastrowid


def select_one_expense(conn, eid: int, uid: int) -> tuple:
    """
    Query an expense by user id

    Parameters:
        conn:       the Connection object
        eid (int):  the user's id
        uid (int):  the expense id

    Return:
        the expense matching eid and uid
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE id=? AND user_id=?",
        (
            eid,
            uid,
        ),
    )

    return cur.fetchone()


def select_expenses_by_uid(conn, uid: int) -> list:
    """
    Query all expenses by user id

    Parameters
        conn:       the Connection object
        uid (int):  ID of user

    Return:
        list of user's expenses as tuples
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=?", (uid,))

    return cur.fetchall()


def delete_one_expense(conn, eid: int, uid: int):
    """
    Delete one of user's expenses

    Parameters
        conn:       the Connection object
        eid (int):  id of expense to delete
        uid (int):  id of user
    """
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM expenses WHERE id=? AND user_id=?",
        (
            eid,
            uid,
        ),
    )
    conn.commit()


def delete_all_user_expense(conn, uid: int):
    """
    Delete all user's expenses

    Parameters
        conn:       the Connection object
        uid (int):  id of user
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE user_id=?", (uid,))
    conn.commit()


def get_all_expenses(conn) -> list:
    """
    Query all expenses

    Parameters
        conn:   the Connection object

    Return:
        list of all expenses as tuples
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")

    return cur.fetchall()


def select_expenses_by_category(conn, uid: int, category: str) -> list:
    """
    Query user expenses by a category

    Parameters:
        conn:           the Connection object
        uid (int):      the user's id
        category (str): the category to filter

    Return:
        list of user expenses filtered by category as tuples
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE user_id=? AND category=?",
        (
            uid,
            category,
        ),
    )

    return cur.fetchall()


def get_total_expenses_by_category(conn, uid: int, category: str) -> int:
    """
    Get the total of all user expenses filtered by category

    Parameters:
        conn:           the Connection object
        uid (int):      the user's id
        category (str): the category to filter

    Return:
        aggregate total amount of the given category
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT amount FROM expenses WHERE user_id=? AND category=?",
        (
            uid,
            category,
        ),
    )

    total = 0
    for row in cur.fetchall():
        total += row[0]

    return total


def get_total_expenses(conn, uid: int) -> int:
    """
    Get the total of all user expenses

    Parameters:
        conn:           the Connection object
        uid (int):      the user's id

    Return:
        aggregate total amount of user expenses
    """
    cur = conn.cursor()
    cur.execute("SELECT amount FROM expenses WHERE user_id=?", (uid,))

    total = 0
    for row in cur.fetchall():
        total += row[0]

    return float("{:.2f}".format(round(total, 2)))
