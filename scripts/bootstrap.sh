#!/bin/bash
export FLASK_APP=./backend/app.py
source $(pipenv --venv)/bin/activate
flask run -h 0.0.0.0