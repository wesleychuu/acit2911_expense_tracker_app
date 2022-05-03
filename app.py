import json
import sqlite3
from flask import Flask, render_template, jsonify, request
from database.sql_db import create_expenses, select_an_expense
from models.expense import Expense
from models.user import User
from models.user_manager import UserManager

app = Flask(__name__)


@app.route("/home/user/<user_id>")
def homepage(user_id):
    """Render the homepage of a user -- shows their expenses"""
    return render_template("home.html")


@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("database.db")
    users = conn.execute('SELECT * FROM users').fetchall()
    conn.close()
    return str(users)


@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("database.db")
    user = conn.execute(
        "SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return str(user)


@app.route("/user/<user_id>/add", methods=["POST"])
def add_expense(user_id):
    """Adds an expense under the user's ID"""
    data = request.json

    try:
        conn = sqlite3.connect("database.db")
        create_expenses(conn, [(f'{data["userid"]}', f'{data["name"]}',
                        f'{data["date"]}', f'{data["category"]}', f'{data["amount"]}')])
        conn.close()
        return "", 201
    except ValueError:
        return "", 400


@app.route("/user/<user_id>/edit/<expense_id>", methods=["GET"])
def get_expense(user_id, expense_id):
    """View an expense by user id and expense id"""
    try:
        conn = sqlite3.connect("database.db")
        expense = select_an_expense(conn, expenseid=expense_id, userid=user_id)
        conn.close()
        return str(expense), 201
    except ValueError:
        return "", 400


@app.route("/user/<uid>/edit/<eid>", methods=["DELETE"])
def delete_expense(eid, uid):
    """Delete an expense by its id"""
    try:
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM expenses WHERE id=? AND user_id=?", (eid, uid,))
        conn.commit()
        conn.close()
        return "", 201
    except ValueError:
        return "", 400


if __name__ == "__main__":
    app.run(debug=True)
