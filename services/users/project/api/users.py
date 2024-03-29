# services/users/project/api/users.py

from flask import Blueprint, jsonify, request
# import requests
from sqlalchemy import exc
from project.api.models import User
from project import db

users_blueprint = Blueprint("users", __name__)


@users_blueprint.route("/ping", methods=["GET"])
def ping_pong():
    return jsonify({
        "status": "success",
        "message": "pong!"
    })


@users_blueprint.route("/users", methods=["POST"])
def add_user():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "%s was added" % email
            }
            return jsonify(response_object), 201
        else:
            response_object["message"] = "Sorry. That email already exists."
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route("/users/<user_id>", methods=["GET"])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {"status": "fail", "message": "User does not exist."}
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                "status": "success",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "active": user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route("/users/login", methods=["POST"])
def login():
    post_data = request.get_json()
    response_object = {
        "status": "fail",
        "message": "Invalid payload."
    }
    if not post_data:
        return jsonify(response_object), 400
    email = post_data.get("email")
    password = post_data.get("password")
    try:
        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            response_object["message"] = "Invalid credentials."
            return jsonify(response_object), 401
        else:
            response_object = {
                "status": "success",
                "message": "User authenticated",
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 400
