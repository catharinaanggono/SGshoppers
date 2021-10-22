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

# -> POST order 
# -> PATCH delivery status
# -> GET by OrderID

class Order_invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_amount = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    delivery_status = db.Column(db.String(200), nullable=False)

    Orders = db.relationship('Order', backref='orders', lazy=True)

    def json(self):
        return {
            "id": self.id, 
            "customer_id": self.customer_id, 
            "total_amount": self.total_amount,
            "deliver_status": self.customer_id
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey(
        'order_invoice.id'), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(6, 2), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def json(self):
        return {
            "id": self.id, 
            "invoice_id": self.invoice_id, 
            "customer_id": self.customer_id, 
            "product_id": self.product_id, 
            "quantity": self.quantity, 
            "price": self.price,
            "created_at": self.created_at
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

    cart = order_data['cart']
    customer_id = order_data['id']
    total_cost = order_data['total_cost']

    #total_cost calculated in FE, pass over
        # total = 0
        # for c_list in cart:
        #     product_price = c_list['unit_price']
        #     total += product_price

    new_order_invoice = Order_invoice(
        customer_id=customer_id, total_amount=total_cost, delivery_status="pending")

    try:
        db.session.add(new_order_invoice)
        db.session.commit()
        invoice_id = new_order_invoice.id
        
    except:
        return jsonify({"status": "fail",
                        "message": "An error occurred creating order invoice."})

    for c_list in cart:
        price = c_list['unit_price']
        product_id = c_list['id']
        quantity = c_list['quantity']
        try:
            new_order = Order(invoice_id=invoice_id, customer_id=customer_id,
                              product_id=product_id, quantity=quantity, price=price)
            db.session.add(new_order)
            db.session.commit()
        except:
            return jsonify({"status": "fail",
                            "message": "An error occurred creating order."})


    return jsonify({"status": "success"})


# -> GET by OrderID
@app.route(url_route + '/get_invoice/', methods=['GET'])
def get_invoice():
    invoice_id = request.args.get('invoice_id')
    invoice = Order_invoice.query.filter_by(id=invoice_id).first()
    if invoice:
        return_message = ({"status": "success",
                           "invoice": invoice.json()})
    else:
        return_message = ({"status": "fail"})
    return jsonify(return_message)


#not sure if we need
    # @app.route(url_route + "/get_all_orders/", methods=['GET'])
    # def get_all_orders():
    #     invoice_id = request.args.get('invoice_id')
    #     order = [order.json()
    #              for order in Order.query.filter_by(invoice_id=invoice_id).all()]
    #     if order:
    #         return_message = ({"status": "success",
    #                            "order": order})
    #     else:
    #         return_message = ({"status": "fail"})
    #     return jsonify(return_message)


# -> PATCH delivery status
@app.route(url_route + "/delivery_status", methods=["PATCH"])
def update_delivery_status(delivery_id):
    json_data = request.get_json()
    delivery_id = json_data["delivery_id"]

    order = Order.query.filter_by(id=delivery_id).first()
    order.delivery_status = "delivered"

    try:
        db.session.commit()
        response = make_response(
            jsonify({"status": "success", "data": {"user": order.json()}}),
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
