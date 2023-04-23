from blog.app import create_app
from blog.models.database import db

app = create_app()


@app.cli.command("init-db", help="create all db")
def init_db():
    db.create_all()
    print("done!")


@app.cli.command("create-users", help="create users")
def create_users():
    from blog.models import User
    admin = User(username="admin", is_staff=True)
    james = User(username="james")
    db.session.add(admin)
    db.session.add(james)
    db.session.commit()
    print("done! created users:", admin, james)
