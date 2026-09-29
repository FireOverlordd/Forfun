from flask import Flask
import os
from flask_mongoengine import MongoEngine
from flask_session.mongodb import MongoDBSessionInterface
from flask_login import LoginManager
from mongoengine.connection import get_db

from .api.auth import auth_bp
from .api.admin import admin_bp
from .api.main import main_bp
from .models.user_model import User

loginManager = LoginManager()
loginManager.login_view = "auth.login"

@loginManager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

    
def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config)

    app.secret_key = os.environ["SECRET_KEY"]

    app.config["MONGODB_SETTINGS"] = {
        "db": "uno_rangliste",
        "host": os.environ["MONGODB_URI"]
    }

    db = MongoEngine()
    db.init_app(app)

    loginManager.init_app(app)

    client = get_db().client
    app.session_interface = MongoDBSessionInterface(
        app,
        client=client,
        permanent=False
    )

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app