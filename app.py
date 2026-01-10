import os
import datetime
from flask import Flask, g, request, redirect, url_for, render_template
from dotenv import load_dotenv
from supabase import create_client, Client

# reads variables from a .env file and sets them in os.environ
load_dotenv()


app = Flask(__name__)

# Load the configuration from the config.DevelopmentConfig module
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

# Load all environment variables starting with a FLASK_ prefix into the *config*
app.config.from_prefixed_env()

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


# register a function to run before each request.
@app.before_request
def load_admin():
    env_admin = os.environ["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.is_admin = True if env_admin == cookies_login else False


def add_pretty_published_at_to_note(note):
    note["published_at_pretty"] = datetime.datetime.fromisoformat(
        note["published_at"]
    ).strftime("%d %B %Y")
    return note


def add_pretty_published_at_to_notes(notes):
    for note in notes:
        add_pretty_published_at_to_note(note)
    return notes


# a decorator which tells the application
# which URL should call the associated function.
@app.route("/")
def index():
    supabase_response = (
        supabase.table("notes")
        .select("*")
        .eq("public", "true")
        .lte("published_at", datetime.datetime.now(datetime.UTC).isoformat())
        .order("published_at", desc=True)
        .execute()
    )
    notes = add_pretty_published_at_to_notes(supabase_response.data)
    return render_template("index.html", notes=notes)


@app.route("/note/<int:id>")
def show(id):
    supabase_response = (
        supabase.table("notes").select("*").eq("id", id).limit(1).single().execute()
    )
    note = add_pretty_published_at_to_note(supabase_response.data)
    return render_template("notes/show.html", note=note)


@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        content = request.form["content"]
        tags = request.form["tags"]
        public = request.form.get("public", default=True)
        supabase.table("notes").insert(
            {"content": content, "tags": tags, "public": public}
        ).execute()
        return redirect(url_for("index"))

    return render_template("notes/new.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    supabase_response = (
        supabase.table("notes").select("*").eq("id", id).limit(1).single().execute()
    )
    note = supabase_response.data

    if request.method == "POST":
        content = request.form["content"]
        tags = request.form["tags"]
        public = request.form.get("public", default=True)

        supabase.table("notes").update(
            {"content": content, "tags": tags, "public": public}
        ).eq("id", id).execute()

        return redirect(url_for("show", id=id))

    return render_template("notes/edit.html", note=note)


@app.route("/delete/<int:id>")
def delete(id):
    supabase.table("notes").delete().eq("id", id).execute()
    return redirect(url_for("index"))


if __name__ == "__main__":
    # run the application on the local dev server
    app.run()
