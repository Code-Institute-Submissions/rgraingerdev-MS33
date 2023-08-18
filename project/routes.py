from flask import Flask, render_template, url_for, request, redirect
from project import app, db

@app.route("/")
def home():
    return render_template("home.html", home=home)

@app.route("/contact")
def contact():
    return render_template("contact.html", contact=contact)

@app.route("/idea3")
def idea3():
    return render_template("idea3.html", idea3=idea3)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("signin.html", signin=signin)


