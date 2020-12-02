from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

db = SQLAlchemy()


class WebPage(db.Model):
    __tablename__ = "d_web_page"

    web_page_id = db.Column(db.Integer(), primary_key=True)
    web_page_name = db.Column(db.String(255))
    web_continent_name = db.Column(db.String(255))
    web_country_code = db.Column(db.String(255))
    web_country_name = db.Column(db.String(255))

    web_region_code = db.Column(db.String(255))
    web_region_name = db.Column(db.String(255))

    web_city = db.Column(db.String(255))
    web_zip = db.Column(db.String(255))

    web_latitude = db.Column(db.Numeric())
    web_longitude = db.Column(db.Numeric())
