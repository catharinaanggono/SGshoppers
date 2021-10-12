from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from datetime import datetime
# from sqlalchemy.sql import func
from os import environ

# import csv
# import sys

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/student_db'

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user_db.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app)


@app.route("/")
def home():
    return "Hello World"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
