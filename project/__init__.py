import os
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env # noqa



app = Flask(__name__)
app.config["secret_key"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL")

db = SQLAlchemy(app)

from project import routes  #noqa


