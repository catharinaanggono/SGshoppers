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


class User_Voucher(db.Model):
    __tablename__ = "user_voucher"

    user_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, value, quantity):
        self.user_id = user_id
        self.value = value
        self.quantity = quantity

    def json(self):
        return {"user_id": self.user_id, "value": self.value, "quantity": self.quantity}


url_route = "/api"


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "Rewards Service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/purchase_voucher", methods=["POST"])
def purchase_voucher():
    data = request.get_json()
    print(data)
    user_id = data["user_id"]
    value = data["value"]
    quantity = data["quantity"]
    user_voucher = (
        User_Voucher.query.filter_by(user_id=user_id).filter_by(value=value).first()
    )
    if user_voucher:
        user_voucher.quantity += quantity
    else:
        user_voucher = User_Voucher(user_id, value, quantity)

    db.session.add(user_voucher)
    db.session.commit()

    return jsonify({"code": 200, "message": "Voucher is successfully purchased"}), 200


@app.route(url_route + "/vouchers/<user_id>")
def get_user_vouchers(user_id):
    user_vouchers = User_Voucher.query.filter_by(user_id=user_id).all()
    if user_vouchers:
        response = make_response(
            jsonify(
                {
                    "status": "success",
                    "data": [user_voucher.json() for user_voucher in user_vouchers],
                }
            ),
            200,
        )
    else:
        response = make_response(
            jsonify({"status": "error", "message": "User does not have vouchers"}),
            404,
        )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/use_voucher/<user_id>/<value>", methods=["PATCH"])
def use_voucher(user_id, value):

    user_voucher = User_Voucher.query.filter_by(user_id=user_id, value=value).first()

    if user_voucher:

        if user_voucher.quantity == 1:
            User_Voucher.query.filter_by(user_id=user_id).filter_by(
                value=value
            ).delete()
        else:
            user_voucher.quantity -= 1

        try:
            db.session.commit()
            response = make_response(
                jsonify(
                    {"status": "success", "message": "Voucher is successfully used."}
                ),
                200,
            )

        except:
            db.session.rollback()
            response = make_response(
                jsonify(
                    {
                        "status": "fail",
                        "message": "An error occurred when updating user's voucher.",
                    }
                ),
                400,
            )
        finally:
            db.session.close()
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "Voucher does not exist."}),
            401,
        )

    response.headers["Content-Type"] = "application/json"
    return response
