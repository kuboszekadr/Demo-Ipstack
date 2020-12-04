import jwt

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from flask import current_app
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()


class WebPage(db.Model):
    __tablename__ = "d_web_page"

    web_id = db.Column(db.Integer(),
                       db.Sequence('d_web_page_web_id_seq'),
                       primary_key=True
                       )
    web_ip = db.Column(db.String(255), primary_key=True)

    web_continent_name = db.Column(db.String(255))
    web_country_code = db.Column(db.String(255))
    web_country_name = db.Column(db.String(255))

    web_region_code = db.Column(db.String(255))
    web_region_name = db.Column(db.String(255))

    web_city = db.Column(db.String(255))
    web_zip = db.Column(db.String(255))

    web_latitude = db.Column(db.Numeric())
    web_longitude = db.Column(db.Numeric())

    last_update = db.Column(db.DateTime())


class User(db.Model):
    __tablename__ = "d_user"

    user_id = db.Column(db.Integer(),
                        db.Sequence('d_user_user_id_seq'),
                        primary_key=True)

    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    @staticmethod
    def hash(password: str) -> str:
        """
        Hashes the provided string to be used as a password

        @param password: string to be hashed

        @returns hashed string
        """
        return sha256.hash(password)

    @staticmethod
    def verify(password: str, hash: str) -> bool:
        """
        docstring
        """
        return sha256.verify(password, hash)

    @classmethod
    def get_user_by_login(cls, login: str):
        return cls.query.filter(cls.login == login).first()
