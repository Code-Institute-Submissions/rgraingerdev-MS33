from flask import render_template
from project import app, db

@app.route("/")
def home():
    return render_template("base.html")

def contact():
    return render_template("contact.html")

def about():
    return render_template("about.html")