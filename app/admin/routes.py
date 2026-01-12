from flask import render_template, redirect, url_for, flash, make_response
from . import admin
from .forms import LoginForm


@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        flash(f"Hello, {username}!", "info")
        resp = make_response(redirect(url_for("main.index")))
        resp.set_cookie("login", username)  # type: ignore
        return resp

    return render_template("admin/login.html", form=form)
