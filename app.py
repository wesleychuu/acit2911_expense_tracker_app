from flask import Flask, render_template, jsonify
from models.expense import Expense
from models.user import User

app = Flask(__name__)


@app.route("/home/user/<user_id>")
def homepage(user_id):
    """Render the homepage of a user -- shows their expenses"""
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
