from dbModel import User, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

from flask import Blueprint, request, Flask, current_app

bp = Blueprint("user", __name__)

@bp.route("/login", methods=["POST"])
def login():
    """
    Login in existing user
    """
    json_data = request.json

    try:
        user_name = json_data['user_name']
        password = json_data['password']
    except KeyError:
        return {'message': 'Bad request'}, 400

    user = User.get_user_by_login(user_name)
    if user is None:
        return {'message': 'User does not exist'}, 404
    elif not User.verify(password, user.password):
        return {'message': 'Password not correct'}, 401

    access_token = create_access_token(identity=user_name)
    return {'message': 'Login succesful',
            'access_token': access_token}, 200


@bp.route("/register", methods=["POST"])
def register():
    """
    Login in existing user
    """
    json_data = request.json

    try:
        user_name = json_data['user_name']
        password = User.hash(json_data['password'])
    except KeyError:
        return {'message': 'Bad request'}, 400

    if User.get_user_by_login(user_name) is not None:
        return {'message': 'User already exists'}, 500

    access_token = create_access_token(identity=user_name)

    user = User(login=user_name, password=password)

    db.session.add(user)
    db.session.commit()

    return {'message': 'User created',
            'access_token': access_token}, 200
