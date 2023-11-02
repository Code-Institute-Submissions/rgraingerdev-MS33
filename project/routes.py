"""Defines routes and uses of pages"""
from flask import render_template, url_for, request, redirect, flash
from flask_login import (login_user, logout_user,
                         LoginManager, current_user, login_required)
import bcrypt
from bcrypt import checkpw
from project.models import Users, Reviews, ContactMessage
from project import app, db

login_manager = LoginManager(app)
login_manager.login_view = 'signin'


@app.route("/")
def home():
    """renders homepage"""
    return render_template("home.html", home=home)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """renders contact form"""
    if request.method == 'POST':
        fname = request.form.get("fname")
        sname = request.form.get("sname")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")
        new_message = ContactMessage(
            fname=fname, sname=sname, email=email,
            subject=subject, message=message
            )
        db.session.add(new_message)
        db.session.commit()

    return render_template("contact.html", contact=contact)


@app.route("/timetable")
@login_required
def timetable():
    """renders Timeline page"""
    return render_template("timetable.html", timetable=timetable)


@app.route("/reviews")
def display_reviews():
    """shows review"""
    review = Reviews.query.join(Users).add_columns(
        Users.fname, Reviews.content, Reviews.id
        ).all()
    return render_template("reviews.html", review=review)


@app.route("/create_message", methods=["GET", "POST"])
def create_message():
    """renders create message page"""
    if request.method == 'POST':

        content = request.form.get("content")

        new_message = Reviews(content=content, user_id=current_user.id)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for("timetable"))
    return render_template("timetable.html", timetable=timetable)


@app.route("/edit_review/<int:review_id>", methods=["GET", "POST"])
def edit_review(review_id):
    """renders review edit"""
    review = Reviews.query.get_or_404(review_id)
    if request.method == 'POST':
        review.content = request.form.get("content")
        db.session.commit()
        return redirect(url_for("timetable"))
    return render_template("edit_review.html", review=review)


@app.route("/delete_review/<int:review_id>")
def delete_review(review_id):
    """deletes review"""
    review = Reviews.query.get_or_404(review_id)

    if review:
        db.session.delete(review)
        db.session.commit()
        return redirect(url_for('timetable'))


@app.route("/view_messages")
def view_messages():
    """view contacts mate to site owner"""
    messages = ContactMessage.query.all()
    return render_template("view_messages.html", messages=messages)


@login_manager.user_loader
def load_user(user_id):
    """loads user details"""
    return Users.query.get(int(user_id))


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """creates user account"""
    if request.method == "POST":
        fname = request.form.get("fname")
        sname = request.form.get("sname")
        email = request.form.get("email")
        password = request.form.get("password")

        pwhash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_password = pwhash.decode('utf-8')

        new_user = Users(
            fname=fname, sname=sname,
            email=email, hashed_password=hashed_password
            )

        db.session.add(new_user)
        db.session.commit()

        flash("Registration Successful", 'success')
        return redirect(url_for("signin"))

    return render_template('signup.html', title="Sign Up", signup=signup)


@app.route("/signin", methods=["GET", "POST"])
def signin():
    """Signs user into site"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter(Users.email == email).first()

        if user and checkpw(
            password.encode('utf-8'), user.hashed_password.encode('utf-8')
        ):
            login_user(user)
            flash("Login Successful", 'success')
            return redirect(url_for("timetable"))
        flash("Login Unsuccessful", 'danger')
    return render_template("signin.html", title="Sign In", signin=signin)


@app.route("/logout")
def logout():
    '''Logs user out'''
    logout_user()
    return redirect(url_for("home"))
