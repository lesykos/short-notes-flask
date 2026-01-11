import os
import datetime
import helpers
from flask import Flask, flash, g, request, abort, redirect, url_for, render_template
from dotenv import load_dotenv
from supabase import create_client, Client
from forms import NoteForm

# reads variables from a .env file and sets them in os.environ
load_dotenv()

# Create an application instance - an object of class Flask
app = Flask(__name__)

# Load the configuration from the config.DevelopmentConfig module
env_config = os.getenv("PROD_APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

# Load all environment variables starting with a FLASK_ prefix into the *config*
app.config.from_prefixed_env()

app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

supabase: Client = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])


# register a function to run before each request.
@app.before_request
def load_admin():
    env_admin = os.environ["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.is_admin = True if env_admin == cookies_login else False


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
    notes = helpers.add_pretty_published_at_to_notes(supabase_response.data)
    return render_template("index.html", notes=notes)


@app.route("/note/<int:id>")
def show(id):
    supabase_response = (
        supabase.table("notes").select("*").eq("id", id).maybe_single().execute()
    )

    if supabase_response is None:
        abort(404)

    note = helpers.add_pretty_published_at_to_note(supabase_response.data)
    return render_template("notes/show.html", note=note)


@app.route("/new", methods=["GET", "POST"])
def new():
    form = NoteForm()
    if form.validate_on_submit():
        content = form.content.data
        tags = form.tags.data
        public = form.public.data

        supabase.table("notes").insert(
            {"content": content, "tags": tags, "public": public}
        ).execute()

        flash("Note created successfully!", "info")
        return redirect(url_for("index"))

    return render_template("notes/new.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    supabase_response = (
        supabase.table("notes").select("*").eq("id", id).maybe_single().execute()
    )
    note = supabase_response.data  # type: ignore

    form = NoteForm(data=note)

    if form.validate_on_submit():
        content = form.content.data
        tags = form.tags.data
        public = form.public.data

        supabase.table("notes").update(
            {"content": content, "tags": tags, "public": public}
        ).eq("id", id).execute()

        flash("Note updated successfully!", "info")
        return redirect(url_for("show", id=id))

    return render_template("notes/edit.html", form=form, note=note)


@app.route("/delete/<int:id>")
def delete(id):
    supabase.table("notes").delete().eq("id", id).execute()
    flash("Note deleted successfully!", "info")
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("error/500.html"), 500


# Older versions of Flask that did not have the *flask* command
# required the server to be started by running the application’s main script.
# Instead we use *flask run* (with *--app hello* if main file isn't named app.py).
# if __name__ == "__main__":
#     # run the application on the local dev server
#     app.run()
