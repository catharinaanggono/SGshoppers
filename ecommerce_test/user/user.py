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
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "role": self.role,
            "created_at": self.created_at,
        }


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "User Service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users")
def users():
    # users = [
    #     {"name": "John", "school": "SCIS"},
    #     {"name": "Jane", "school": "SCIS"},
    #     {"name": "Richard ", "school": "SCIS"},
    # ]

    users = {"user": [User.json() for User in User.query.all()]}
    response = make_response(
        jsonify({"status": "success", "data": users}),
        200,
    )

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
