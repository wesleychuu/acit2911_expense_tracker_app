import sqlite3

def insert_user(conn, name, username, email, password):
    """
    Create user and insert into the users table

    Parameters:
        conn:   Connection object
        name:   user's name
        username:   user's username
        email:      user's email
        password:   user's password, hashed

    Return:
        id of last row
    """
    sql = ''' INSERT INTO users(name,username,email,password) VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, (name,username,email,password,))
    conn.commit()

    return cur.lastrowid

def select_all_users(conn):
    """
    Query all users

    Parameters: 
        conn: the Connection object
    
    Return:
        list of all users
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    return str(cur.fetchall())


def select_user_by_id(conn, uid):
    """
    Query user by user id
    :param conn: the Connection object
    :param userid: a user's id
    :return: 
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (uid,))

    return str(cur.fetchone())

def delete_user_by_id(conn, uid):
    """
    Delete a user by id

    Parameters: 
        conn:   Connection object
        uid:    id of user to delete
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id=?", (uid,))
    conn.commit()
