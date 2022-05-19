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


def update_expense(conn, eid: int, name: str, category: str, amount: str, date: str):
    """
    Update the given expense with the given information 

    Parameters:
        conn:           the Connection object
        eid (int):      the expense id
        name (str):     name of the expense
        category (str): category of the expense
        amount (str):   amount of the expense
        date (str):     date of the expense
    """
    cur = conn.cursor()
    cur.execute(
        "UPDATE expenses SET name=?, category=?, amount=?, date=? WHERE id=?",
        (name, category, amount, date, eid,)
    )
    conn.commit()


def get_user_categories(conn, uid: int) -> list:
    """
    Get the categories that users have expenses in

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id

    Return:
        A list of the user's expense categories
    """
    cur = conn.cursor()
    cat = cur.execute("SELECT category FROM expenses WHERE user_id=?", (uid,))
    cat = set(cat)

    categories = []
    if cat:
        for c in cat:
            categories.append(c[0])

    return sorted(categories)


def get_expense_today(conn, uid: int) -> tuple:
    """
    Get the list of user expenses recorded today, along with the total

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id

    Return:
        A tuple consisting of the user's list of expenses made today and the total
    """
    cur = conn.cursor()
    exp = cur.execute(
        "SELECT * FROM expenses WHERE DATE(date) = DATE('now') AND user_id=?", (uid,))
    today_exp = exp.fetchall()

    total = 0
    if today_exp:
        for e in today_exp:
            total += e[5]

    return total, today_exp


def get_expense_week(conn, uid: int) -> tuple:
    """
    Get the list of user expenses recorded in the past 7 days, along with the total

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id

    Return:
        A tuple consisting of the user's list of expenses in the past week and the total
    """
    cur = conn.cursor()
    exp = cur.execute(
        "SELECT * FROM expenses WHERE DATE(date) >= DATE('now', '-7 day') AND user_id=?", (uid,))
    week_exp = exp.fetchall()

    total = 0
    if week_exp:
        for e in week_exp:
            total += e[5]

    return total, week_exp


def get_expense_month(conn, uid: int) -> tuple:
    """
    Get the list of user expenses recorded in the past 30 days, along with the total

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id

    Return:
        A tuple consisting of the user's list of expenses in the past 30 days and the total
    """
    cur = conn.cursor()
    exp = cur.execute(
        "SELECT * FROM expenses WHERE DATE(date) >= DATE('now', '-30 day') AND user_id=?", (uid,))
    month_exp = exp.fetchall()

    total = 0
    if month_exp:
        for e in month_exp:
            total += e[5]

    return total, month_exp


def get_expense_keyword(conn, uid: int, kw: str) -> tuple:
    """
    Get the list of user expenses where name matches a given keyword, along with the total

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id
        kw (str):   the keyword string to match

    Return:
        A tuple consisting of the user's list of expenses matching the keyword and the total
    """
    cur = conn.cursor()
    exp = cur.execute(
        "SELECT * FROM expenses WHERE name LIKE '%'||?||'%' AND user_id=?", (kw, uid,))
    kw_exp = exp.fetchall()

    total = 0
    if kw_exp:
        for e in kw_exp:
            total += e[5]

    return total, kw_exp


def get_expense_category(conn, uid: int, category: str) -> tuple:
    """
    Get the list of user expenses where category matches a given category, along with the total

    Parameters:
        conn:       the Connection object
        uid (int):  the user's id
        kw (str):   the category to match

    Return:
        A tuple consisting of the user's list of expenses matching the category and the total
    """
    cur = conn.cursor()
    exp = cur.execute(
        "SELECT * FROM expenses WHERE category LIKE '%'||?||'%' AND user_id=?", (category, uid,))
    category_exp = exp.fetchall()

    total = 0
    if category_exp:
        for e in category_exp:
            total += e[5]

    return total, category_exp


def get_expense_today(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM expenses WHERE date BETWEEN DATE('now')-1 AND DATE('now')")
    return cur.fetchall()
