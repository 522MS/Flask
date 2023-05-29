from flask import Flask, render_template
from flask_migrate import Migrate

from blog.admin import admin
from blog.api import init_api
from blog.article.views import article
from blog.auth.views import auth, login_manager
from blog.author.views import author
from blog.models.database import db
from blog.security import flask_bcrypt
from blog.user.views import user
import os


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SECRET_KEY"] = '(paroyb8#%g!s$9el79a4o(iv8&dg%y%txml+@ya=k^jhh6*g%'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    cfg_name = os.environ.get("CONFIG_NAME") or "BaseConfig"
    app.config.from_object(f"blog.configs.{cfg_name}")

    migrate = Migrate()
    migrate.init_app(app, db, compare_type=True)

    flask_bcrypt.init_app(app)

    admin.init_app(app)

    api = init_api(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    app.register_blueprint(user)
    app.register_blueprint(article)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(author, url_prefix="/authors")
    login_manager.init_app(app)

    @app.cli.command("create-tags")
    def create_tags():
        """
        Run in your terminal:
        ➜ flask create-tags
        """
        from blog.models import Tag
        for name in [
            "flask",
            "django",
            "python",
            "sqlalchemy",
            "news",
        ]:
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
        print("created tags")

    return app
