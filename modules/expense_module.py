import sqlite3

def insert_expense(conn, uid, name, date, category, amount):
    """
    Insert a new expense into expenses table

    Parameters:
        conn:       the Connection obj
        uid:        user id
        name:       title of expense
        date:       date of expense
        category:   type of expense
        amount:     amount of expense
    
    Return:
        id of last row
    """
    sql = ''' INSERT INTO expenses(user_id,name,date,category,amount) VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (uid,name,date,category,amount,))
    conn.commit()

    return cur.lastrowid

def get_one_expense(conn, eid, uid):
    """
    Query an expense by user id

    Parameters:
        conn:   the Connection object
        eid:    the user's id
        uid:    the expense id
    
    Return: 
        the expense matching eid and uid
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE id=? AND user_id=?",
                (eid, uid,))

    return str(cur.fetchone())

def get_all_user_expenses(conn, uid) -> list:
    """
    Query all expenses by user id

    Parameters
        conn:   the Connection object
        uid:    ID of user
    
    Return: 
        list of user's expenses
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=?", (uid,))

    return str(cur.fetchall())

def delete_an_expense(conn, eid, uid):
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?", (eid, uid,))
    conn.commit()

def delete_all_user_expense(conn, uid):
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE user_id=?", (uid,))
    conn.commit()

def get_all_expenses(conn):
    """
    Query all expenses

    Parameters
        conn:   the Connection object
    
    Return: 
        list of all expenses
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses")

    return str(cur.fetchall())