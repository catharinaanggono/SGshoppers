#!/bin/bash
export FLASK_ENV=development
export FLASK_APP=user.py
flask db init
flask db migrate
flask db upgrade
flask run --host=0.0.0.0 --port=5000
