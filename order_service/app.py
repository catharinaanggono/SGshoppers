from os import environ

from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate
from flask_cors import CORS

<<<<<<< HEAD
import boto3

=======
>>>>>>> parent of 4ac3bb3 (Add SNS boto3 codes)
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("dbURL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

# -> POST order
# -> PATCH delivery status
# -> GET by OrderID


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(
        db.Integer, db.ForeignKey("order_invoice.id"), nullable=False
    )
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String(120), nullable=False)
    product_name = db.Column(db.String(64), nullable=False)
    product_image = db.Column(db.String(64), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(6, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def __init__(
        self,
        id,
        invoice_id,
        customer_id,
        product_id,
        product_name,
        product_image,
        quantity,
        price,
        created_at,
    ):
        self.id = id
        self.invoice_id = invoice_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_image = product_image
        self.quantity = quantity
        self.price = price
        self.created_at = created_at

    def json(self):
        return {
            "id": self.id,
            "invoice_id": self.invoice_id,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_image": self.product_image,
            "quantity": self.quantity,
            "price": self.price,
            "created_at": self.created_at,
        }


class Order_invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_amount = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    delivery_status = db.Column(db.String(200), nullable=False)

    Orders = db.relationship("Order", backref="orders", lazy=True)

    def __init__(self, id, total_amount, customer_id, delivery_status):
        self.id = id
        self.total_amount = total_amount
        self.customer_id = customer_id
        self.delivery_status = delivery_status

    def json(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "total_amount": self.total_amount,
            "delivery_status": self.delivery_status,
        }


url_route = "/api"


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "ORDER Service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/create_order", methods=["POST"])
def create_order():
    order_data = request.get_json()

    cart = order_data["cart"]
    customer_id = order_data["customer_id"]
    total_amount = order_data["total_amount"]

    # total_cost calculated in FE, pass over
    # total = 0
    # for c_list in cart:
    #     product_price = c_list['unit_price']
    #     total += product_price
    invoice = Order_invoice(None, total_amount, customer_id, "Pending")

    try:
        db.session.add(invoice)
        db.session.commit()
        invoice_id = invoice.id
    except:
        return jsonify(
            {
                "status": "fail",
                "message": "An error occurred when creating order invoice.",
            }
        )

    for item in cart:
        order = Order(
            None,
            invoice_id,
            customer_id,
            item["pId"],
            item["pName"],
            item["pImg"],
            item["quantity"],
            item["price"],
            datetime.now(),
        )
        try:
            db.session.add(order)
            db.session.commit()
        except:
            return jsonify(
                {
                    "status": "fail",
                    "message": "An error occurred when creating order",
                }
            )

    return jsonify({"status": "success", "message": invoice.json()})


@app.route(url_route + "/invoice/<int:id>", methods=["GET"])
def get_invoice(id):
    invoice = Order_invoice.query.filter_by(id=id).first()
    if invoice:
        return jsonify({"status": "success", "data": invoice.json()})
    return jsonify({"status": "fail", "message": "Invoice not found."})


@app.route(url_route + "/invoices/<int:customer_id>", methods=["GET"])
def get_customer_invoices(customer_id):
    invoices = Order_invoice.query.filter_by(customer_id=customer_id).all()
    if len(invoices):
        return jsonify(
            {
                "status": "success",
                "data": {"invoices": [invoice.json() for invoice in invoices]},
            }
        )
    return jsonify({"status": "fail", "message": "There are no invoices."})


@app.route(url_route + "/invoices", methods=["GET"])
def get_all_invoices():
    invoices = Order_invoice.query.all()
    if len(invoices):
        return jsonify(
            {
                "status": "success",
                "data": {"invoices": [invoice.json() for invoice in invoices]},
            }
        )
    return jsonify({"status": "fail", "message": "There are no invoices."})


# -> PATCH delivery status
@app.route(url_route + "/invoice/<int:id>/delivery_status", methods=["PATCH"])
def update_delivery_status(id):
    invoice = Order_invoice.query.filter_by(id=id).first()
    invoice.delivery_status = "delivered"

    try:
        db.session.commit()
        response = make_response(jsonify({"status": "success", "data": invoice.json()}))
    except:
        db.session.rollback()
        response = make_response(
            jsonify(
                {
                    "status": "fail",
                    "message": "An error occurred when updating delivery status",
                }
            )
        )
    finally:
        db.session.close()

    response.headers["Content-Type"] = "application/json"
    return response
