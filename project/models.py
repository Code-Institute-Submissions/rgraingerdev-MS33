"""Table modles creation"""
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import bcrypt
from project import db


class Users(UserMixin, db.Model):
    """Creates user table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)


    def get_user_by_id(self, user_id):
        """returns user id"""
        return Users.query.get(int(user_id))

class ContactMessage(db.Model):
    """Creates contact table"""
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique = True, nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable = False)

class Reviews(db.Model):
    """creates review table"""
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable = False)
    user = relationship("Users", backref="Reviews", primaryjoin="users.id == Reviews.user_id")

if __name__ == "__main__":
    print("Creating Database Tables...")
    db.create_all()
    print("Done!")
