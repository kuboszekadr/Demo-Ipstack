import socket

from .models import Ipstack
from flask import Blueprint, request, Flask, json, current_app
from dbModel import WebPage, db


bp = Blueprint("api", __name__)


@bp.route("/api", methods=["GET"])
def get_webpage_info():
    """
    Gets information about webpage from ipstack
    """
    json_data = request.json
    url = json_data['url']
    if url is None:
        return '500'

    return '1'


@ bp.route("/api", methods=["POST"])
def add_webpage_info():
    """
    Puts webpage data into database (data is fetched from ipstack)
    """
    json_data = request.json
    url = json_data['url']
    if url is None:
        return '500'

    # if ip adress is passed do nothing
    try:
        url = socket.inet_aton(url)
    except socket.error:
        # else convert to ip address
        url = socket.gethostbyname(url)

    if is_url_in_db(url):
        return '208'  # already reported

    # get data from ipstack
    ipstack = Ipstack.Ipstack(current_app.config["SECRET_KEY"])
    results = ipstack.fetch_data_about_url(url)

    # get only relevant fields
    results = {x: results[x] for x in current_app.config['IPSTACK_FIELDS']}
    add_new_url(results)  # add url into db

    return '201'  # created


@ bp.route("/api", methods=["DELETE"])
def delete_webpage_info():
    """
    Deleted cached data about webpage from the database
    """
    json_data = request.json
    url = json_data['url']

    return '200'


def add_new_url(results: dict):
    """
    Adds new url into database
    """
    wp = WebPage(
        **{'web_{}'.format(field): results[field]
           for field in results.keys()}
    )
    db.session.add(wp)
    db.session.commit()


def is_url_in_db(ip: str) -> bool:
    """
    Checks if provided ip is in db

    @param ip - ip adress to be searched for

    @returns True / False 
    """
    is_url_in_db = WebPage.query.with_entities(
        WebPage.web_id
    ).filter(WebPage.web_ip == ip).\
        first()

    return False if is_url_in_db is None else True
