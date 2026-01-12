import datetime
from flask import current_app, render_template
from app.notes.helpers import (
    add_pretty_published_at_to_notes,
    add_pretty_tags_to_notes,
    get_all_tags_from_notes,
)
from app.tags import tags


@tags.route("/")
def index():
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    supabase_response = (
        supabase_client.table("notes").select("tags").eq("public", "true").execute()
    )
    tags = get_all_tags_from_notes(supabase_response.data)

    return render_template("tags/index.html", tags=tags)


@tags.route("/<string:tag>")
def show(tag):
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    current_datetime_str = datetime.datetime.now(datetime.UTC).isoformat()
    supabase_response = (
        supabase_client.table("notes")
        .select("*")
        .ilike("tags", f"%{tag}%")
        .eq("public", "true")
        .lte("published_at", current_datetime_str)
        .order("published_at", desc=True)
        .execute()
    )
    notes = add_pretty_published_at_to_notes(supabase_response.data)
    notes = add_pretty_tags_to_notes(notes)
    page_heading = f"Notes with tag #{tag}"

    return render_template("index.html", notes=notes, page_heading=page_heading)
