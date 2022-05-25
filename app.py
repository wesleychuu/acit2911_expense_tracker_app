from datetime import date
import re
import sqlite3
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect, url_for, session, flash
from modules.app_helper_module import *
from modules.expense_module import *
from modules.user_module import *
from models.user import User
from models.login_form import LoginForm
from models.register_form import RegisterForm
from models.reset_password import ResetPasswordForm
from models.search_form import SearchForm
from sql_db import create_connection
from models.expense import Expense
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "Thisisspposedtobesecret"
Bootstrap(app)


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        try:
            conn = create_connection("database.db")
            user = select_user_by_username(conn, form.username.data)
            if not user or user[4] != str(
                hashlib.sha256(form.password.data.encode()).hexdigest()
            ):
                flash("Incorrect username or password", category="alert-warning")
            else:
                if user[4] == str(hashlib.sha256(form.password.data.encode()).hexdigest()):
                    session["uid"] = user[0]
                    return redirect(url_for("homepage")), 301
        finally:
            conn.close()

    return render_template("login.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        try:
            conn = create_connection("database.db")

            existing_username = select_user_by_username(conn, form.username.data)
            existing_email = select_user_by_email(conn, form.email.data.lower())
            # check if username/email is taken
            if existing_username:
                flash("Username already taken.")
            elif existing_email:
                flash("Email already registered.")
            else:
                # create a new User to validate
                new_user = User(
                    name=form.name.data,
                    username=form.username.data,
                    email=form.email.data.lower(),
                    password=form.password.data,
                )

                # insert user into db
                insert_user(
                    conn,
                    new_user.name,
                    new_user.username,
                    new_user.email,
                    new_user.password,
                )

            flash(
                "Great success! New account has been created.", category="alert-success"
            )
            return redirect(url_for("login"))
        finally:
            conn.close()

    return render_template("signup.html", form=form), 200


@app.route("/home", methods=["GET", "POST"])
def homepage():
    """Render the homepage of a user -- shows their expenses"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    try:
        conn = create_connection("database.db")
        tuple_expenses = select_expenses_by_uid(conn, session["uid"])
        pie_data = get_pie_data(conn, session["uid"])
        total_expense = get_total_expenses(conn, session["uid"])
    finally:
        conn.close()

    user_expenses = sorted([data_to_dict(each_expense) for each_expense in tuple_expenses],
                           key=lambda d: d["date"], reverse=True)

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            if request.form.get("filter_all"):
                return redirect(url_for("homepage")), 301
            else:
                eid = data["expense_to_delete"]
                delete_one_expense(conn, eid, session["uid"])
                return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template(
            "home.html",
            user_expenses=user_expenses,
            total_expense=str(total_expense),
            data=pie_data,
        ),
        200,
    )


@app.route("/home/today", methods=["GET", "POST"])
def homepage_today():
    """Render the homepage of a user -- shows their expenses from the past 24 hours or from today only"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    try:
        conn = create_connection("database.db")
        # Should select the expenses by uid AND (within 24 hours or from today's date)
        tuple_expenses = get_expense_today(conn, session["uid"])
        pie_data = get_pie_data(conn, session["uid"])
        total_expense = tuple_expenses[0]
    finally:
        conn.close()

    user_expenses = sorted([data_to_dict(each_expense) for each_expense in tuple_expenses[1]],
                           key=lambda d: d["date"], reverse=True)

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            if request.form.get("filter_today"):
                return redirect(url_for("homepage_today")), 301
            else:
                eid = data["expense_to_delete"]
                delete_one_expense(conn, eid, session["uid"])
                return redirect(url_for("homepage_today")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template(
            "home_today.html",
            user_expenses=user_expenses,
            total_expense=str(total_expense),
            data=pie_data,
        ),
        200,
    )


@app.route("/home/week", methods=["GET", "POST"])
def homepage_week():
    """Render the homepage of a user -- shows their expenses from this week or the past 168 hours"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    try:
        conn = create_connection("database.db")
        # Should select the expenses by uid AND (within 168 hours or from this week)
        tuple_expenses = get_expense_week(conn, session["uid"])
        pie_data = get_pie_data(conn, session["uid"])
        total_expense = tuple_expenses[0]
    finally:
        conn.close()

    user_expenses = sorted([data_to_dict(each_expense) for each_expense in tuple_expenses[1]],
                           key=lambda d: d["date"], reverse=True)

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            if request.form.get("filter_week"):
                return redirect(url_for("homepage_week")), 301
            else:
                eid = data["expense_to_delete"]
                delete_one_expense(conn, eid, session["uid"])
                return redirect(url_for("homepage_week")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template(
            "home_week.html",
            user_expenses=user_expenses,
            total_expense=str(total_expense),
            data=pie_data,
        ),
        200,
    )


@app.route("/home/month", methods=["GET", "POST"])
def homepage_month():
    """Render the homepage of a user -- shows their expenses from this month"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    try:
        conn = create_connection("database.db")
        # Should select the expenses by uid AND from this month
        tuple_expenses = get_expense_month(conn, session["uid"])
        pie_data = get_pie_data(conn, session["uid"])
        total_expense = tuple_expenses[0]
    finally:
        conn.close()

    user_expenses = sorted([data_to_dict(each_expense) for each_expense in tuple_expenses[1]],
                           key=lambda d: d["date"], reverse=True)

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            if request.form.get("filter_month"):
                return redirect(url_for("homepage_month")), 301
            else:
                eid = data["expense_to_delete"]
                delete_one_expense(conn, eid, session["uid"])
                return redirect(url_for("homepage_month")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template(
            "home_month.html",
            user_expenses=user_expenses,
            total_expense=str(total_expense),
            data=pie_data,
        ),
        200,
    )


@app.route("/home/year", methods=["GET", "POST"])
def homepage_year():
    """Render the homepage of a user -- shows their expenses from this year"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    try:
        conn = create_connection("database.db")
        # Should select the expenses by uid AND from this year
        tuple_expenses = get_expense_year(conn, session["uid"])
        pie_data = get_pie_data(conn, session["uid"])

        total_expense = tuple_expenses[0]
    finally:
        conn.close()

    user_expenses = sorted([data_to_dict(each_expense) for each_expense in tuple_expenses[1]],
                           key=lambda d: d["date"], reverse=True)

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            if request.form.get("filter_year"):
                return redirect(url_for("homepage_year")), 301
            else:
                eid = data["expense_to_delete"]
                delete_one_expense(conn, eid, session["uid"])
                return redirect(url_for("homepage_year")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template(
            "home_year.html",
            user_expenses=user_expenses,
            total_expense=str(total_expense),
            data=pie_data,
        ),
        200,
    )


@app.route("/add", methods=["GET", "POST"])
def add_page():
    """Adds an expense under the user's ID"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    data = request.form
    conn = create_connection("database.db")
    today = date.today()
    if request.method == "POST":
        try:
            ex1 = Expense(
                data["name"], data["date"], data["category"], float(
                    data["amount"])
            )
            insert_expense(
                conn, session["uid"], ex1.name, ex1.date, ex1.category, ex1.amount
            )
            return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return render_template("add_expense.html", today=today), 200


@app.route("/edit/<eid>", methods=["GET", "POST"])
def get_expense(eid):
    """View an expense by user id and expense id for editing"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    today = date.today()
    
    try:
        conn = create_connection("database.db")
        expense = select_one_expense(conn, eid, session["uid"])
    finally:
        conn.close()
        
    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        try:
            update_expense(
                conn, eid, data["name"], data["category"], data["amount"], data["date"])
            return redirect(url_for("homepage")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template("edit_expense.html",
                        expense=expense, uid=session["uid"], today=today),
        200,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    try:
        conn = create_connection("database.db")
        user = select_user_by_id(conn, session["uid"])
        name = user[1]
        username = user[2]
        email = user[3]
    finally:
        conn.close()

    if request.method == "POST":
        conn = create_connection("database.db")
        try:
            delete_all_user_expense(conn, session["uid"])
            delete_user_by_id(conn, session["uid"])
            flash("Account deleted -- Sorry to see you go :(",
                  category="alert-success")
            return redirect(url_for("login")), 301
        except ValueError:
            return "", 400
        finally:
            conn.close()

    return (
        render_template("profile.html", name=name,
                        username=username, email=email),
        200,
    )


@app.route("/logout", methods=["POST"])
def logout():
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    session.pop("uid", None)
    flash("You are logged out", category="alert-success")
    return redirect(url_for("login"))


@app.route("/profile/edit", methods=["GET", "POST"])
def profile_edit():
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    try:
        conn = create_connection("database.db")
        user = select_user_by_id(conn, session["uid"])
        name = user[1]
        username = user[2]
        email = user[3]
    finally:
        conn.close()

    if request.method == "POST":
        conn = create_connection("database.db")
        data = request.form
        existing_username = select_user_by_username(conn, data["username"])
        existing_email = select_user_by_email(conn, data["email"])

        if existing_username and existing_username != user:
            flash("Username already taken", category="alert-success")
        elif existing_email and existing_email != user:
            flash("Email already registered", category="alert-success")
        # elif len(data["username"]) < 5:
        #     flash("Username too short", category="alert-success")
        # elif "@" not in data["email"]:
        #     flash("Invalid email", category="alert-success")
        elif "." not in data["email"]:
            flash("Invalid email", category="alert-success")
        else:
            update_user(conn, session["uid"], data["name"],
                        data["username"], data["email"])
            return redirect("/profile"), 301
    return render_template("edit_profile.html", name=name, username=username, email=email), 200


@app.route("/profile/resetpassword", methods=["GET", "POST"])
def reset_password():
    """Delete a user's expense by its id"""
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))
    
    form = ResetPasswordForm()

    if request.method == "POST":
        if form.validate_on_submit():
            try:
                conn = create_connection("database.db")
                user = select_user_by_id(conn, session["uid"])
                if user[4] == str(
                    hashlib.sha256(form.old_password.data.encode()).hexdigest()
                ):
                    update_password(
                        conn,
                        session["uid"],
                        str(
                            hashlib.sha256(
                                form.new_password.data.encode()).hexdigest()
                        ),
                    )
                    session["uid"] = None
                    flash(
                        "Great success! Password was reset, please log in again.",
                        category="alert-success",
                    )
                    return redirect("/"), 301
            finally:
                conn.close()

    return render_template("reset_password.html", form=form, uid=session["uid"]), 200


@app.route("/search", methods=["GET", "POST"])
def search():
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    form = SearchForm()

    try:
        conn = sqlite3.connect("database.db")
        categories = get_user_categories(conn, session["uid"])
    finally:
        conn.close()

    if request.method == "POST":
        if form.validate_on_submit():
            searched = form.searched.data
            return redirect(url_for("search_result_kw", searched=searched))

    return render_template("search.html", form=form, categories=categories), 200


@app.route("/search?search=<searched>", methods=["GET", "POST"])
def search_result_kw(searched):
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    form = SearchForm()

    try: 
        conn = create_connection("database.db")
        if re.match("20", searched):
            total, expenses = get_expense_date_search(
                conn, session["uid"], searched)
        else:
            total, expenses = get_expense_keyword(conn, session["uid"], searched)
    finally:
        conn.close()

    expenses = sorted([data_to_dict(e) for e in expenses],
                      key=lambda d: d["date"], reverse=True)

    return render_template("search.html", form=form, searched=searched, total=total, expenses=expenses), 200


@app.route("/search?category=<searched>", methods=["GET", "POST"])
def search_result_category(searched):
    if not check_session(session["uid"]):
        flash("You must be logged in to view this page",  category="alert-warning")
        return redirect(url_for("login"))

    form = SearchForm()

    try:
        conn = create_connection("database.db")
        total, expenses = get_expense_category(conn, session["uid"], searched)
    finally:
        conn.close()

    expenses = sorted([data_to_dict(e) for e in expenses],
                      key=lambda d: d["date"], reverse=True)

    return render_template("search.html", form=form, searched=searched, total=total, expenses=expenses), 200


if __name__ == "__main__":
    app.run(debug=True)
