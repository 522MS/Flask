from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello web!"


@app.route("/power/<int:x>/<int:y>")
def power_value(x, y):
    result = x ** y
    return f"{result}"


@app.route("/user/")
def read_user():
    name = request.args.get("name")
    surname = request.args.get("surname")
    return f"User {name or '[no name]'} {surname or '[no surname]'}"
