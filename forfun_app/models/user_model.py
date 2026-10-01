from forfun_app.database.db import db
from flask_login import UserMixin

class User(db.Document, UserMixin):
    username = db.StringField(max_length=128, required=True)
    password = db.StringField(max_length=128, required=True)
    is_admin = db.BooleanField(default=False)