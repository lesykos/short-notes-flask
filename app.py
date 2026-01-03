import datetime
from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)

class Note(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(200))
    published: Mapped[bool] = mapped_column(nullable=False, insert_default=True)
    published_at: Mapped[datetime.date] = mapped_column(nullable=False, insert_default=datetime.date.today())

    # define the object's class name and key attributes
    # making it easy to understand the object's state in Debugging and Inspection.
    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, published={self.published})"

# a decorator which tells the application
# which URL should call the associated function.
@app.route("/")
def index():
    notes = db.session.execute(db.select(Note).order_by(Note.published_at)).scalars()
    return render_template("index.html", notes = notes)

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        note = Note(content=request.form["content"])
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("notes/new.html")

if __name__ == "__main__":
    # run the application on the local dev server
    app.run(debug=True)
