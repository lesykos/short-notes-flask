import os
import datetime
from flask import Flask, g, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from dotenv import load_dotenv

# reads variables from a .env file and sets them in os.environ
load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)
# configure from Environment Variables
app.config.from_prefixed_env()
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

# s


class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(200))
    published: Mapped[bool] = mapped_column(nullable=False, insert_default=True)
    published_at: Mapped[datetime.datetime] = mapped_column(
        nullable=False, insert_default=datetime.datetime.now()
    )

    # define the object's class name and key attributes
    # making it easy to understand the object's state in Debugging and Inspection.
    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, published={self.published})"


# register a function to run before each request.
@app.before_request
def load_admin():
    env_admin = app.config["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.is_admin = True if env_admin == cookies_login else False


# a decorator which tells the application
# which URL should call the associated function.
@app.route("/")
def index():
    notes = db.session.execute(db.select(Note).order_by(Note.id.desc())).scalars()
    return render_template("index.html", notes=notes)


@app.route("/note/<int:id>")
def show(id):
    note = db.get_or_404(Note, id)
    return render_template("notes/show.html", note=note)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        note = Note(content=request.form["content"])  # type: ignore
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("notes/new.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    note = db.get_or_404(Note, id)

    if request.method == "POST":
        note.content = request.form["content"]
        db.session.commit()
        return redirect(url_for("show", id=note.id))

    return render_template("notes/edit.html", note=note)


@app.route("/delete/<int:id>")
def delete(id):
    note = db.get_or_404(Note, id)

    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # run the application on the local dev server
    # debug=True
    app.run()
