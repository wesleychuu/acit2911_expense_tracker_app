from flask import Flask, render_template, jsonify
from models.expense import Expense
from models.user import User

app = Flask(__name__)


@app.route("/home")
def homepage():
    return render_template("home.html")


@app.route("/user/<user_id>")
def user(user_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
