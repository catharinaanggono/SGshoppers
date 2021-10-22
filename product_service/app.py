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


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "image": self.image
        }


url_route = "/api"


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "Product Service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/product/<product_id>")
def get_product_by_id(product_id):
    product = Product.query.filter_by(id=product_id).first()
    if product:
        response = make_response(
            jsonify({"status": "success", "data": {"product": product.json()}}),
            200,
        )
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "Fail to retrive product"}),
            404,
        )

    response.headers["Content-Type"] = "application/json"
    return response


@app.route(url_route + "/product_search/<keyword>")
def get_product_by_name(keyword):
    print(keyword)
    products = Product.query.filter(Product.name.ilike(f'%{keyword}%'))
    print("PRODUCTS - ", products)

    if products:
        response = make_response(
            jsonify(
                {
                    "status": "success",
                    "products": [product.json() for product in products]
                }
            ),
            200,
        )
    else:
        response = make_response(
            jsonify({"status": "fail", "message": "No product with this keyword found"}),
            404,
        )

    response.headers["Content-Type"] = "application/json"
    return response
