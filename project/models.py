"""Table modles creation"""
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from project import db


class Users(UserMixin, db.Model):
    """Creates user table"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def get_user_by_id(self, user_id):
        """returns user id"""
        return Users.query.get(int(user_id))


class ContactMessage(db.Model):
    """Creates contact table"""
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(60), nullable=False)
    message = db.Column(db.Text, nullable=False)


class Reviews(db.Model):

    """creates review table"""
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False
        )
    user = relationship("Users", backref="Reviews")


if __name__ == "__main__":
    print("Creating Database Tables...")
    db.create_all()
    print("Done!")
