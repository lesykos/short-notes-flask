import functools
from flask import (
    g,
    current_app,
    request,
    redirect,
    render_template,
    abort,
    flash,
    url_for,
)
from .helpers import (
    add_pretty_published_at_to_note,
    add_pretty_tags_to_note,
)
from .forms import NoteForm
from app.notes import notes


# register a function to run before each request.
@notes.before_request
def load_user():
    env_admin = current_app.config["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.current_user = cookies_login
    g.current_user_is_admin = True if env_admin == cookies_login else False


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not g.current_user_is_admin:
            return redirect(url_for("main.index"))

        return view(**kwargs)

    return wrapped_view


@notes.route("/<int:id>")
def show(id):
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    supabase_response = (
        supabase_client.table("notes").select("*").eq("id", id).maybe_single().execute()
    )

    if supabase_response is None:
        abort(404)

    note = add_pretty_published_at_to_note(supabase_response.data)
    note = add_pretty_tags_to_note(note)
    return render_template("notes/show.html", note=note)


@notes.route("/new", methods=["GET", "POST"])
@admin_required
def new():
    form = NoteForm()
    supabase_client = current_app.config["SUPABASE_CLIENT"]

    if form.validate_on_submit():
        content = form.content.data
        tags = form.tags.data
        public = form.public.data
        published_at = form.published_at.data

        supabase_client.table("notes").insert(
            {
                "content": content,
                "tags": tags,
                "public": public,
                "published_at": published_at.isoformat(),  # type: ignore
            }
        ).execute()

        flash("Note created successfully!", "info")
        return redirect(url_for("main.index"))

    return render_template("notes/new.html", form=form)


@notes.route("/edit/<int:id>", methods=["GET", "POST"])
@admin_required
def edit(id):
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    supabase_response = (
        supabase_client.table("notes").select("*").eq("id", id).maybe_single().execute()
    )
    note = supabase_response.data  # type: ignore

    form = NoteForm(data=note)

    if form.validate_on_submit():
        content = form.content.data
        tags = form.tags.data
        public = form.public.data
        published_at = form.published_at.data

        supabase_client.table("notes").update(
            {
                "content": content,
                "tags": tags,
                "public": public,
                "published_at": published_at.isoformat(),  # type: ignore
            }
        ).eq("id", id).execute()

        flash("Note updated successfully!", "info")
        return redirect(url_for("notes.show", id=id))

    return render_template("notes/edit.html", form=form, note=note)


@notes.route("/delete/<int:id>")
@admin_required
def delete(id):
    supabase_client = current_app.config["SUPABASE_CLIENT"]
    supabase_client.table("notes").delete().eq("id", id).execute()
    flash("Note deleted successfully!", "info")
    return redirect(url_for("main.index"))
