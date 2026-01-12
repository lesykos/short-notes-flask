from flask import render_template, redirect, url_for, flash
from . import admin
from .forms import LoginForm


@admin.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        # TODO: Set cookie or session here
        flash(f"Hello, {username}!", "info")
        return redirect(url_for("main.index"))

    return render_template("admin/login.html", form=form)
