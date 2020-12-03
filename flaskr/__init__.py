from flask import Flask
from configparser import ConfigParser
from flask_sqlalchemy import SQLAlchemy


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from .api import api
    from dbModel import db
    app.register_blueprint(api.bp)

    config = ConfigParser()
    config.read(r'.\config.ini')

    app.config['SECRET_KEY'] = config['SECRET']['secret_key']
    app.config['IPSTACK_FIELDS'] = eval(config['DATA']['fields'])

    app.config['SQLALCHEMY_DATABASE_URI'] = config['DATABASE']['uri']

    db.init_app(app)
    return app
