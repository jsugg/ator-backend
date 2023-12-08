#!/bin/bash
export FLASK_APP=run.py
flask db upgrade
flask db init
flask db migrate
flask db upgrade
