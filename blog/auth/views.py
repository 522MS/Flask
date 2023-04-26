from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import LoginManager, login_user, login_required, logout_user

from blog.models import User

auth = Blueprint('auth', __name__, url_prefix='/auth', static_folder='../static')
login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth.login"))


__all__ = [
    "login_manager",
    "auth",
]


@auth.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    username = request.form.get("username")
    if not username:
        return render_template("auth/login.html", error="username not passed")
    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        return render_template("auth/login.html", error=f"no user {username!r} found")
    login_user(user)
    return redirect(url_for("user.user_list"))


@auth.route("/logout", endpoint="logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/secret")
@login_required
def secret_view():
    return "Super secret data"
