from flask import (
    g,
    current_app,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    make_response,
)
from . import auth
from .forms import LoginForm


# register a function that runs before the view function,
# no matter what URL is requested.
@auth.before_app_request
def load_user():
    env_admin = current_app.config["ADMIN_NAME"]
    cookies_login = request.cookies.get("login")
    g.current_user = cookies_login
    g.current_user_is_admin = True if env_admin == cookies_login else False


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash(f"Hello, {username}!", "info")
        resp = make_response(redirect(url_for("main.index")))
        resp.set_cookie("login", username)  # type: ignore
        return resp

    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    flash("You have been logged out.", "info")
    resp = make_response(redirect(url_for("main.index")))
    resp.delete_cookie("login")
    return resp
