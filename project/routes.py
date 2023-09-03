from flask import Flask, render_template, url_for, request, redirect
from project import app, db
from sqlalchemy import text


@app.route("/")
def home():
    return render_template("home.html", home=home)

@app.route("/contact")
def contact():
    return render_template("contact.html", contact=contact)

@app.route("/messages")
def messages():
    return render_template("messages.html", messages=messages)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    return render_template("signin.html", title="Sign IN", signin = signin)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get("fname")
        sname = request.form.get("sname")
        password_hash = request.form.get("password")
        email = request.form.get("email")

        new_user = users(fname = fname, sname = sname, email = email)
        new_user.set_password(password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("messages"))
    return render_template("signup.html", title="Sign Up", signin=signin)


@app.route('/test-connection')
def test_connection():
    try:
        count = text('SELECT COUNT(*) FROM users')
        return f"Connection successful! Total records: {count}"
    except Exception as e:
        return f"Connection failed: {str(e)}"
    



