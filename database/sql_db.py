import sqlite3
import json
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    """
    Create a new user into the users table
    :param conn:
    :param user:
    :return: user id
    """
    with open("../data/users.json", "w") as fp:
        pass

    sql = ''' INSERT INTO users(name,username,email,password)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


def create_expense(conn, expense):
    """
    Create a new expense
    :param conn:
    :param expense:
    :return:
    """

    sql = ''' INSERT INTO expenses(user_id,name,date,category,amount)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, expense)
    conn.commit()

    return cur.lastrowid


def main():
    database = "database.db"

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        username text NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL
                                    ); """

    sql_create_expenses_table = """CREATE TABLE IF NOT EXISTS expenses (
                                    user_id integer NOT NULL,
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    date numeric NOT NULL,
                                    category text NOT NULL,
                                    amount numberic NOT NULL,
                                    FOREIGN KEY (user_id) REFERENCES users (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_users_table)

        # create tasks table
        create_table(conn, sql_create_expenses_table)
    else:
        print("Error! cannot create the database connection.")

    with conn:
        # create a new user
        user = ('Test Dummy', 'testdummy',
                'testdummy@testmail.ca', 'Testing123@')
        user_id = create_user(conn, user)

        # expenses
        expense_1 = (user_id, 'Coffee', '2022-01-01', 'Food', 4.50)
        expense_2 = (user_id, 'Laptop', '2022-02-30', 'Technology', 1200.00)

        # create expenses
        create_expense(conn, expense_1)
        create_expense(conn, expense_2)


if __name__ == '__main__':
    main()
