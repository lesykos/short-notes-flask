import datetime
from flask import g, current_app, request, render_template
from app.notes.helpers import (
    add_pretty_published_at_to_notes,
    add_pretty_tags_to_notes,
)

# Here app is the project’s package,
# main is the main blueprint package
from app.main import main


# register a function to run before each request.
@main.before_request
def load_admin():
    env_admin = current_app.config["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.is_admin = True if env_admin == cookies_login else False


@main.route("/")
def index():
    # Access the Supabase client from the current application context
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    current_datetime_str = datetime.datetime.now(datetime.UTC).isoformat()
    supabase_response = (
        supabase_client.table("notes")
        .select("*")
        .eq("public", "true")
        .lte("published_at", current_datetime_str)
        .order("published_at", desc=True)
        .execute()
    )
    notes = add_pretty_published_at_to_notes(supabase_response.data)
    notes = add_pretty_tags_to_notes(notes)
    return render_template("index.html", notes=notes)
