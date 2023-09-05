from project import db
import bcrypt
from datetime import datetime
from flask_login import Loginmanager, usermixin, login_user, Login_required, Logout_user, Current_user

class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(20), nullable=False)
    sname = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120),unique=True, nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


login_manager = Loginmanager(app)
login_manager.login_view = 'login'

def load_user(user_id):
    return users.query.get(int(user_id))


def message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable = False)

    user = db.relationship('users', backref=db.backref('messages', Lazy=True))


db.create_all()



