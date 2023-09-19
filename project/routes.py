from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import login_user, logout_user, LoginManager, current_user, UserMixin, login_required
from flask_sqlalchemy import SQLAlchemy
from project import app, db
from sqlalchemy import text
from project.models import users, reviews, ContactMessage
import bcrypt
from bcrypt import hashpw, gensalt, checkpw

login_manager = LoginManager(app)
login_manager.login_view = 'signin'

@app.route("/")
def home():
    return render_template("home.html", home=home)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        fname = request.form.get("fname")
        sname = request.form.get("sname")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        new_message = ContactMessage(fname=fname, sname=sname, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()

    return render_template("contact.html", contact=contact)

@app.route("/timetable")
@login_required
def timetable():
    return render_template("timetable.html", timetable=timetable)

@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    if request.method == 'POST':

        content = request.form.get("content")

        new_message = reviews(content=content, user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("timetable"))
    return render_template("timetable.html", timetable=timetable)

@app.route("/view_messages")
def view_messages():
    messages = ContactMessage.query.all()
    return render_template("view_messages.html", messages=messages)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get("fname")
        sname = request.form.get("sname")
        email = request.form.get("email")
        password = request.form.get("password")

        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_password = pwhash.decode('utf-8')

        new_user = users(fname=fname, sname=sname, email=email, hashed_password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful", 'success')
        return redirect(url_for("signin"))
    
    return render_template('signup.html', title="Sign Up", signup=signup)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = users.query.filter(users.email == email).first()

        if user and checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            login_user(user)
            flash("Login Successful", 'success')
            return redirect(url_for("messages"))
        flash("Login Unsuccessful", 'danger')
    return render_template("signin.html", title="Sign In", signin=signin)
            
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/test-connection')
def test_connection():
    try:
        count = text('SELECT * FROM users')
        return f"Connection successful! Total records: {count}"
    except Exception as e:
        return f"Connection failed: {str(e)}"
    



