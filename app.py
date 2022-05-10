import sqlite3
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, session
from modules.expense_module import *
from modules.user_module import *
from models.login_form import LoginForm
from models.register_form import RegisterForm
from sql_db import create_connection
from models.expense import CATEGORIES, Expense

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisspposedtobesecret"
Bootstrap(app)


def data_to_dict(data_tup: tuple) -> dict:
    return {
        "name": data_tup[2],
        "date": data_tup[3],
        "category": data_tup[4],
        "amount": data_tup[5],
    }


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    conn = create_connection("database.db")

    if form.validate_on_submit():
        user = select_user_by_username(conn, form.username.data)
        if user:
            if user[4] == form.password.data:
                session["uid"] = user[0]
                return redirect(url_for("homepage", uid=session["uid"]))

        return "<h1>Invalid username or password</h1>"

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    # if form.validate_on_submit():
    #     new_user = User(name=form.name.data, username=form.username.data,
    #                     email=form.email.data, password=form.password.data)
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for('login'))

    return render_template("signup.html", form=form)


@app.route("/user/<uid>")
def homepage(uid):
    """Render the homepage of a user -- shows their expenses"""
    conn = create_connection("database.db")
    tuple_expenses = select_expenses_by_uid(conn, uid)

    total_category_exp = []
    for category in CATEGORIES:
        total_category_exp.append(get_total_expenses_by_category(conn, uid, category))

    total_expense = get_total_expenses(conn, uid)
    conn.close()

    user_expenses = [data_to_dict(each_expense) for each_expense in tuple_expenses]

    pie_data = {
        "Category": "Amount",
        "Food": total_category_exp[0],
        "Apparel": total_category_exp[1],
        "Entertainment": total_category_exp[2],
        "Lifestyle": total_category_exp[3],
        "Miscellaneous": total_category_exp[4],
        "Groceries": total_category_exp[5],
        "Services": total_category_exp[6],
        "Technology": total_category_exp[7],
        "School": total_category_exp[8],
    }

    return render_template(
        "home.html",
        user_expenses=user_expenses,
        total_expense=str(total_expense),
        data=pie_data,
    )


@app.route("/user/<uid>/add", methods=["GET"])
def load_add_page(uid):
    return render_template("add_expense.html")


@app.route("/user/<uid>/add", methods=["POST"])
def add_expense(uid):
    """Adds an expense under the user's ID"""
    data = request.form
    conn = create_connection("database.db")

    try:
        ex1 = Expense(data["name"], data["date"], data["category"], data["amount"])
        insert_expense(conn, uid, ex1.name, ex1.date, ex1.category, ex1.amount)
        return redirect(f"/user/{uid}"), 301
    except ValueError:
        return "", 400
    finally:
        conn.close()


@app.route("/user/<uid>/edit/<eid>", methods=["GET"])
def get_expense(uid, eid):
    """View an expense by user id and expense id for editing"""
    conn = create_connection("database.db")

    try:
        expense = select_one_expense(conn, eid=eid, uid=uid)
        return str(expense), 201
    except ValueError:
        return "", 400
    finally:
        conn.close()


@app.route("/user/<uid>/edit/<eid>", methods=["DELETE"])
def delete_expense(eid, uid):
    """Delete an expense by its id"""
    conn = create_connection("database.db")

    try:
        delete_one_expense(conn, eid, uid)
        return "", 201
    except ValueError:
        return "", 400
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(debug=True)
