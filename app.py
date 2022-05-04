import sqlite3
from flask import Flask, render_template, request
from modules.expense_module import *
from modules.user_module import *

app = Flask(__name__)


def data_to_dict(data_tup: tuple) -> dict:
    return {
        "name": data_tup[2],
        "date": data_tup[3],
        "category": data_tup[4],
        "amount": data_tup[5]
    }

@app.route("/home/user/<uid>")
def homepage(uid):
    """Render the homepage of a user -- shows their expenses"""
    conn = sqlite3.connect("database.db")
    tuple_expenses = select_expenses_by_uid(conn, uid)
    conn.close()
    user_expenses = [data_to_dict(each_expense) for each_expense in tuple_expenses]
    
    # total_expense = 0.0

    return render_template("home.html", user_expenses = user_expenses)


@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("database.db")
    users = select_all_users(conn)
    conn.close()
    return str(users)


@app.route("/user/<uid>", methods=["GET"])
def get_user(uid):
    conn = sqlite3.connect("database.db")
    user = select_user_by_id(conn, uid)
    conn.close()
    return str(user)


@app.route("/user/<uid>/add", methods=["POST"])
def add_expense(uid):
    """Adds an expense under the user's ID"""
    data = request.json

    try:
        conn = sqlite3.connect("database.db")
        insert_expense(conn, (uid, f'{data["name"]}',
                        f'{data["date"]}', f'{data["category"]}', f'{data["amount"]}'))
        conn.close()
        return "", 201
    except ValueError:
        return "", 400


@app.route("/user/<uid>/edit/<eid>", methods=["GET"])
def get_expense(uid, eid):
    """View an expense by user id and expense id"""
    try:
        conn = sqlite3.connect("database.db")
        expense = select_one_expense(conn, eid=eid, uid=uid)
        conn.close()
        return str(expense), 201
    except ValueError:
        return "", 400


@app.route("/user/<uid>/edit/<eid>", methods=["DELETE"])
def delete_expense(eid, uid):
    """Delete an expense by its id"""
    try:
        conn = sqlite3.connect("database.db")
        delete_one_expense(conn, eid, uid)
        conn.close()
        return "", 201
    except ValueError:
        return "", 400


if __name__ == "__main__":
    app.run(debug=True)
