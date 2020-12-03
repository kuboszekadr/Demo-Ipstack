import socket

from .models import Ipstack
from flask import Blueprint, request, Flask, json, current_app, jsonify
from dbModel import WebPage, db


bp = Blueprint("api", __name__)
error_code_str = '{{"error_code": {error_code}, "brief": "{brief}"}}'


@bp.route("/api", methods=["GET"])
def get_webpage_info():
    """
    Gets information about webpage from ipstack
    """
    json_data = request.json
    url = json_data['url']

    if url is None:
        return error_code_str.format(error_code="500", brief="Empty url")

    ip = url_to_ip(url)
    ip_id = get_ip_id(ip)

    if ip_id == 0:
        return error_code_str.format(error_code=404, brief="Ip url is not in the database")

    # Get data for found ip id
    result = WebPage.query.filter(WebPage.web_id == ip_id).first()

    # convert result into dict
    result = {field: result.__dict__["web_" + field]
              for field in current_app.config['IPSTACK_FIELDS']}

    return json.dumps(result, ensure_ascii=False, default=str)


@ bp.route("/api", methods=["POST"])
def add_webpage_info():
    """
    Puts webpage data into database (data is fetched from ipstack)
    """
    json_data = request.json
    url = json_data['url']
    if url is None:
        return error_code_str.format(error_code=500, brief="Empty url")

    # unify provided address
    ip = url_to_ip(url)

    if get_ip_id(ip) > 0:
        return error_code_str.format(error_code=209, brief="Ip already exists")

    # get data from ipstack
    ipstack = Ipstack.Ipstack(current_app.config["SECRET_KEY"])
    results = ipstack.fetch_data_about_url(ip)

    # get only relevant fields
    results = {x: results[x] for x in current_app.config['IPSTACK_FIELDS']}
    add_new_url(results)  # add url into db

    return error_code_str.format(error_code=200, brief="Record created")


@ bp.route("/api", methods=["DELETE"])
def delete_webpage_info():
    """
    Deleted cached data about webpage from the database
    """
    json_data = request.json
    url = json_data['url']

    return error_code_str.format(error_code=200, brief="Record deleted")


def add_new_url(data: dict):
    """
    Adds new url into database

    @param data: dict of url fields to be added into DB 

    @returns: None
    """
    wp = WebPage(
        **{'web_{}'.format(field): data[field]
           for field in data.keys()}
    )
    db.session.add(wp)
    db.session.commit()


def get_ip_id(ip: str) -> int:
    """
    Gets ip id in DB

    @param ip: ip adress to be searched for

    @returns: int of ip id > 0 if exists else 0
    """
    ip_id = WebPage.query.with_entities(
        WebPage.web_id
    ).filter(WebPage.web_ip == ip).\
        first()

    return 0 if ip_id is None else ip_id.web_id


def url_to_ip(url: str) -> str:
    """
    Converts url to ip. If IP provided returns it

    @param url: url address to be converted into ip

    @returns ip adress of url 
    """

    # if ip adress is passed do nothing
    try:
        url = socket.inet_aton(url)
    except socket.error:
        # else convert to ip address
        url = socket.gethostbyname(url)

    return url
