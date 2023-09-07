from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, LoginManager, current_user
from project import app, db
from sqlalchemy import text
from project.models import users, message
login_manager = LoginManager(app)
login_manager.login_view = 'signin'

@app.route("/")
def home():
    return render_template("home.html", home=home)

@app.route("/contact")
def contact():
    return render_template("contact.html", contact=contact)

@app.route("/messages")
def messages():
    return render_template("messages.html", messages=messages)

@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    if request.method == "POST":
        content = request.form.get("content")
        user = current_user()
        new_message = messages(content=content, user=user)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("messages"))
    return render_template("create_message.html", create_message=create_message)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.query.filter_by(email=email).first()
        if email and user.check_password(password):
            login_user(user)

            return redirect(url_for("messages"))
        else:
            flash("invalid credentials", "error")
            return redirect(url_for("signin"))

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
    



