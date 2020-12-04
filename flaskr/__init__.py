import os
from configparser import ConfigParser

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

jwt = JWTManager()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from .api import api, user
    from dbModel import db
    app.register_blueprint(api.bp)
    app.register_blueprint(user.bp)

    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
    app.config['IPSTACK_FIELDS'] = eval(os.environ.get("DATA_FIELDS"))

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    app.config['JWT'] = os.environ.get("JWT_SECRET")

    db.init_app(app)
    jwt.init_app(app)

    return app
