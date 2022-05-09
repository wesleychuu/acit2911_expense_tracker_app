import sqlite3


def insert_user(conn, name: str, username: str, email: str, password: str) -> int:
    """
    Create user and insert into the users table

    Parameters:
        conn:           the Connection object
        name (str):     user name
        username (str): user username
        email (str):    user email
        password (str): user password, hashed

    Return:
        id of last row
    """
    sql = ''' INSERT INTO users(name,username,email,password) VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, (name, username, email, password,))
    conn.commit()

    return cur.lastrowid


def select_all_users(conn) -> list:
    """
    Query all users

    Parameters: 
        conn: the Connection object

    Return:
        list of all users as tuples
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    return cur.fetchall()


def select_user_by_id(conn, uid: str) -> tuple:
    """
    Query user by user id

    Parameters: 
        conn:       the Connection object
        uid (int):  id of user to find

    Return:
        a user and their information as a tuple
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))

    return cur.fetchone()


def delete_user_by_id(conn, uid: int):
    """
    Delete a user by id

    Parameters: 
        conn:       the Connection object
        uid (int):  id of user to delete
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()


def select_user_by_username(conn, username):
    """
    Query a user by username

    Parameters: 
        conn:       the Connection object
        username:   username of user to find
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))

    return cur.fetchone()
