from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def test():
    response = make_response(
        jsonify({"status": "success", "message": "user service is working"}),
        200,
    )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/users")
def users():
    users = [
        {"name": "John", "school": "SCIS"},
        {"name": "Jane", "school": "SCIS"},
        {"name": "Richard ", "school": "SCIS"},
    ]
    response = make_response(
        jsonify({"status": "success", "data": users}),
        200,
    )

    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
