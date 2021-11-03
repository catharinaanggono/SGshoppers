from os import environ

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "points": self.points,
            "created_at": self.created_at,
        }


url_route = "/api"


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "User Service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/user/authenticate", methods=["POST"])
def authenticate():
    user_json = request.get_json()
    email = user_json["email"]
    password = user_json["password"]
    user = User.query.filter_by(email=email).first()
    if user:
        if password == user.password:
            response = make_response(
                jsonify({"status": "success", "data": {"user": user.json()}}),
                200,
            )
        else:
            response = make_response(
                jsonify({"status": "fail", "message": "Invalid Password"}),
                401,
            )
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "Invalid Email"}),
            401,
        )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/user/<user_id>")
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        response = make_response(
            jsonify({"status": "success", "data": {"user": user.json()}}),
            200,
        )
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "User does not exist"}),
            200,
        )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/users")
def list_users():
    users = {"users": [User.json() for User in User.query.all()]}
    response = make_response(
        jsonify({"status": "success", "data": users}),
        200,
    )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/user/<user_id>/points", methods=["GET"])
def get_user_points(user_id):
    user = User.query.filter_by(id=user_id).first()
    points = user.points
    if user:
        response = make_response(
            jsonify({"status": "success", "data": {"points": points}}),
            200,
        )
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "User does not exist"}),
            200,
        )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/user/<user_id>/points", methods=["PATCH"])
def update_user_points(user_id):
    json_data = request.get_json()
    points = json_data["points"]

    user = User.query.filter_by(id=user_id).first()
    user.points = points

    try:
        db.session.commit()
        response = make_response(
            jsonify({"status": "success", "data": {"user": user.json()}}),
            200,
        )
    except:
        db.session.rollback()
        response = make_response(
            jsonify(
                {"status": "fail", "message": "An error occurred when updating points."}
            ),
            400,
        )
    finally:
        db.session.close()

    response.headers["Content-Type"] = "application/json"
    return response
