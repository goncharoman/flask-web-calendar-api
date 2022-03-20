# load flask
from flask import Flask

# import api's
from . import api
from .db import db


def create_app():
    """Create current app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    app.register_blueprint(api.v1.api, url_prefix="/api/v1")
    app.register_blueprint(api.v2.api, url_prefix="/api/v2")
    with app.app_context():
        db.create_all()
    return app
