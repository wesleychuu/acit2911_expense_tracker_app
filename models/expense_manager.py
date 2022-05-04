import sqlite3
from sqlite3 import Error
from sql_db import *

class ExpenseManager:
    def __init__(self):
        conn = sqlite3.connect("database.db")
        self.expenses = conn.execute('SELECT * FROM expenses').fetchall()
        conn.close()

    def insert_expense(self, conn, uid, name, date, category, amount):
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
        cur.executemany(sql, (uid,name,date,category,amount,))
        conn.commit()

        return cur.lastrowid
    
    def get_an_expense(self, conn, eid, uid):
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

        return cur.fetchone()

    def get_all_expenses(self, conn, uid) -> list:
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

        return cur.fetchall()

    def remove_expense(self, eid)