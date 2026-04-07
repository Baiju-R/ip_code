"""Simple Flask login app with a light/dark theme toggle."""

from __future__ import annotations

import os

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "dev-only-secret-key")

# Demo users for local development.
# In real applications, store users in a database.
VALID_USERS = {
    "admin": generate_password_hash("admin123"),
    "user": generate_password_hash("password"),
}


@app.get("/")
def index() -> str:
    return render_template("index.html", user=session.get("user"))


@app.post("/login")
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    stored_hash = VALID_USERS.get(username)
    if stored_hash and check_password_hash(stored_hash, password):
        session["user"] = username
        flash("Login successful.", "success")
        return redirect(url_for("index"))

    flash("Invalid username or password.", "error")
    return redirect(url_for("index"))


@app.post("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
