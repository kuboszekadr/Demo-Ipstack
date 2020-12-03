from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql
from flask import current_app

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


class User(db.Model):
    __tablename__ = "d_user"

    user_id = db.Column(db.Integer(), primary_key=True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))
