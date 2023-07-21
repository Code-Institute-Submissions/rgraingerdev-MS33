from flask import render_template, url_for
from project import app, db

@app.route("/")
def home():
    return render_template("home.html", home=home)

@app.route("/contact")
def contact():
    return render_template("contact.html", contact=contact)

@app.route("/about")
def about():
    return render_template("about.html", about=about)

@app.route("/signin")
def signin():
    return render_template("signin.html", signin=signin)