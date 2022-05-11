import sqlite3
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modules.expense_module import *
from modules.user_module import *
from models.user import User
from models.login_form import LoginForm
from models.register_form import RegisterForm
from models.reset_password import ResetPasswordForm
from sql_db import create_connection
from models.expense import CATEGORIES, Expense
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisspposedtobesecret"
Bootstrap(app)


def data_to_dict(data_tup: tuple) -> dict:
    return {
        "name": data_tup[2],
        "date": data_tup[3],
        "category": data_tup[4],
        "amount": data_tup[5],
        "eid": data_tup[0]
    }


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    conn = create_connection("database.db")

    if form.validate_on_submit():
        user = select_user_by_username(conn, form.username.data)
        if not user or user[4] != str(hashlib.sha256(form.password.data.encode()).hexdigest()):
            flash("Inccorrect username or password")
        else:
            if user[4] == str(hashlib.sha256(form.password.data.encode()).hexdigest()):
                session["uid"] = user[0]
                return redirect(url_for("homepage")), 301

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        conn = create_connection("database.db")

        existing_username = select_user_by_username(conn, form.username.data)
        existing_email = select_user_by_email(conn, form.email.data)

        # check if username is taken
        # check if email taken
        if existing_username:
            flash("Username already taken")
        elif existing_email:
            flash("Email already registered")
        else:
            # create a new User to validate
            new_user = User(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                password=form.password.data,
            )

            # insert user into db
            insert_user(
                conn, new_user.name, new_user.username, new_user.email, new_user.password
            )

            conn.close()
            return redirect(url_for("login"))

    return render_template("signup.html", form=form), 200


@app.route("/home", methods=["GET", "POST"])
def homepage():
    """Render the homepage of a user -- shows their expenses"""
    conn = create_connection("database.db")
    tuple_expenses = select_expenses_by_uid(conn, session["uid"])

    total_category_exp = []
    for category in CATEGORIES:
        total_category_exp.append(
            get_total_expenses_by_category(conn, session["uid"], category))

    total_expense = get_total_expenses(conn, session["uid"])
    conn.close()

    user_expenses = [data_to_dict(each_expense)
                     for each_expense in tuple_expenses]

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

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        eid = data["expense_to_delete"]
        try:
            delete_one_expense(conn, eid, session['uid'])
            return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return render_template(
        "home.html",
        user_expenses=user_expenses,
        total_expense=str(total_expense),
        data=pie_data,
    ) , 200


@app.route("/add", methods=["GET", "POST"])
def add_page():
    """Adds an expense under the user's ID"""
    data = request.form
    conn = create_connection("database.db")

    if request.method == "POST":
        try:
            ex1 = Expense(data["name"], data["date"], data["category"], float(data["amount"]))
            insert_expense(conn, session["uid"], ex1.name, ex1.date, ex1.category, ex1.amount)
            return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()
    
    return render_template("add_expense.html"), 200


@app.route("/edit/<eid>", methods=["GET", "POST"])
def get_expense(eid):
    """View an expense by user id and expense id for editing"""
    conn = create_connection("database.db")
    expense = select_one_expense(conn, eid, session["uid"])

    if request.method == "POST":
        try:
            return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()
    
    return render_template("edit_expense.html", expense=expense, uid=session["uid"]), 200


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html"), 200


@app.route("/profile/edit", methods=["GET", "POST"])
def profile():
    return render_template("edit_profile.html"), 200


@app.route("/profile/resetpassword", methods=["GET", "POST"])
def reset_password():
    """Delete a user's expense by its id"""
    form = ResetPasswordForm()
    conn = create_connection("database.db")

    if request.method == "POST":
        if form.validate_on_submit():
            user = select_user_by_id(conn, session['uid'])
            if user[4] == str(hashlib.sha256(form.old_password.data.encode()).hexdigest()):
                try:
                    update_password(conn, session['uid'], str(hashlib.sha256(form.new_password.data.encode()).hexdigest()))
                    session['uid'] = None
                    return redirect("/"), 301
                except ValueError:
                    return "", 400
                finally:
                    conn.close()
    
    return render_template("reset_password.html", form=form, uid=session['uid']), 200

if __name__ == "__main__":
    app.run(debug=True)
