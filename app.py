import sqlite3
from flask import Flask, render_template, request
from modules.expense_module import *
from modules.user_module import *
from models.expense import CATEGORIES

app = Flask(__name__)


def data_to_dict(data_tup: tuple) -> dict:
    return {
        "name": data_tup[2],
        "date": data_tup[3],
        "category": data_tup[4],
        "amount": data_tup[5]
    }


@app.route("/user/<uid>")
def homepage(uid):
    """Render the homepage of a user -- shows their expenses"""
    conn = sqlite3.connect("database.db")
    tuple_expenses = select_expenses_by_uid(conn, uid)

    total_category_exp = []
    for category in CATEGORIES:
        total_category_exp.append(
            get_total_expenses_by_category(conn, uid, category))

    total_expense = get_total_expenses(conn, uid)
    conn.close()

    user_expenses = [data_to_dict(each_expense)
                     for each_expense in tuple_expenses]

    return render_template("home.html", user_expenses=user_expenses, total_category_exp=total_category_exp, total_expense=str(total_expense))


@app.route("/user/<uid>/add", methods=["GET"])
def load_add_page(uid):
    return render_template("add_expense.html")


@app.route("/user/<uid>/add", methods=["POST"])
def add_expense(uid):
    """Adds an expense under the user's ID"""
    data = request.json

    try:
        conn = sqlite3.connect("database.db")
        insert_expense(conn, uid, f'{data["name"]}',
                       f'{data["date"]}', f'{data["category"]}', f'{data["amount"]}')
        conn.close()
        return "", 201
    except ValueError:
        return "", 400


@app.route("/user/<uid>/edit/<eid>", methods=["GET"])
def get_expense(uid, eid):
    """View an expense by user id and expense id for editing"""
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


# @app.route("/users", methods=["GET"])
# def get_users():
#     conn = sqlite3.connect("database.db")
#     users = select_all_users(conn)
#     conn.close()
#     return str(users)


# @app.route("/user/<uid>", methods=["GET"])
# def get_user(uid):
#     conn = sqlite3.connect("database.db")
#     user = select_user_by_id(conn, uid)
#     conn.close()
#     return str(user)


if __name__ == "__main__":
    app.run(debug=True)
