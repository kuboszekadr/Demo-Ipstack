from .models import Ipstack
from flask import Blueprint, request, Flask, json, current_app

bp = Blueprint("api", __name__)


@bp.route("/api", methods=["GET"])
def get_webpage_info():
    """
    Gets information about webpage from ipstack
    """
    return '200'


@bp.route("/api", methods=["POST"])
def add_webpage_info():
    """
    Puts webpage data into database (data is fetched from ipstack)
    """
    json_data = request.json
    url = json_data['url']
    if url is None:
        return '500'

    ipstack = Ipstack.Ipstack(current_app.config["SECRET_KEY"])
    results = ipstack.fetch_data_about_url(url)

    return json.dumps(results)


@bp.route("/api", methods=["DELETE"])
def delete_webpage_info():
    """
    Deleted cached data about webpage from the database
    """
    return '201'
