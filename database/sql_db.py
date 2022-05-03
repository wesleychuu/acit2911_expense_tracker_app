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


def create_users(conn, users: list):
    """
    Create users and insert into the users table
    :param conn: Connection object
    :param users: list of users to insert
    :return:
    """
    query = ''' INSERT INTO users(name,username,email,password)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(query, users)
    conn.commit()

    return cur.lastrowid


def create_expenses(conn, expenses: list):
    """
    Create expenses and insert into expenses table
    :param conn: Connection object
    :param expenses: list of expenses to insert
    :return:
    """
    sql = ''' INSERT INTO expenses(user_id,name,date,category,amount)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.executemany(sql, expenses)
    conn.commit()

    return cur.lastrowid


def populate_table(conn, name, json_data):
    """
    Populate database tables with given json data
    :param conn: Connection object
    :param name: a string identifying what type json data is (users or expenses)
    :param json_data: json data to be convereted and inserted
    :return:
    """
    with conn:
        columns = []
        column = []
        for data in json_data:
            column = list(data.keys())
            for col in column:
                if col not in columns:
                    columns.append(col)

        value = []
        values = []
        for data in json_data:
            for i in columns:
                value.append(str(dict(data).get(i)))
            values.append(list(value))
            value.clear()

        if name == "users":
            create_users(conn, values)

        if name == "expenses":
            create_expenses(conn, values)
            print(values)


def select_all_users(conn):
    """
    Query all rows in the users table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")

    return cur.fetchall()


def select_user_by_id(conn, userid):
    """
    Query user by user id
    :param conn: the Connection object
    :param userid: a user's id
    :return: 
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (userid,))

    return cur.fetchone()


def select_expenses_by_userid(conn, userid) -> list:
    """
    Query expenses by user id
    :param conn: the Connection object
    :param userid: a user's id
    :return: list of user expenses
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE user_id=?", (userid,))

    return cur.fetchall()


def select_an_expense(conn, expenseid, userid):
    """
    Query expenses by user id
    :param conn: the Connection object
    :param userid: a user's id
    :param expenseid: an expense's id
    :return: the expense matching userid and expenseid
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM expenses WHERE id=? AND user_id=?",
                (expenseid, userid,))

    return cur.fetchone()


def delete_expense(conn, id_tuple):
    """
    Delete an epense by user id and expense id
    :param conn:  Connection to the SQLite database
    :param userid: id of the user
    :param expenseid: id of the expense
    :return:
    """
    (eid, uid) = id_tuple
    cur = conn.cursor()
    cur.execute("DELETE FROM expenses WHERE id=? AND user_id=?",
                (eid, uid,))
    conn.commit()


def main():
    database = "database.db"
    users_json = json.load(open("../data/users.json"))
    expenses_json = json.load(open("../data/expenses.json"))

    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        username text UNIQUE NOT NULL,
                                        email text NOT NULL,
                                        password text NOT NULL
                                    ); """

    sql_create_expenses_table = """CREATE TABLE IF NOT EXISTS expenses (
                                    id integer PRIMARY KEY,
                                    user_id integer NOT NULL,
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
        # Populate users table with user json data
        populate_table(conn, "users", users_json)
        # Populate expenses table with expenses json data
        populate_table(conn, "expenses", expenses_json)


if __name__ == '__main__':
    main()
