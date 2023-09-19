from project import db
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
import bcrypt


class users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)

    def get_user_by_id(user_id):
        return users.query.get(int(user_id))

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable = False)

class message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    user = db.relationship('users', backref=db.backref('messages', lazy=True))

if __name__ == "__main__":
    print("Creating Database Tables...")
    db.create_all()
    print("Done!")



