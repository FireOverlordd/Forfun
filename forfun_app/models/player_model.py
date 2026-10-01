from forfun_app.database.db import db

class Player(db.Document):
    name = db.StringField(max_length=128, required=True)
    wins = db.IntField(required=True)