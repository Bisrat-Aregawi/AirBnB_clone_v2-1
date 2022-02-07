#!/usr/bin/python3
"""Creationg route for Blueprint
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify

@app_views.route('/status')
def response():
    """ get status ok
    """
    dic = {"status": "OK"}
    return dic
@app_views.route('/stats')
def db_stats():
    """ retrieve and show number of each objects by type
    """
    dictionary = {
        "amenities": 0,
        "cities": 0,
        "places": 0,
        "reviews": 0,
        "states": 0,
        "users": 0,
    }
    for v in storage.all().values():
        dictionary[v.__tablename__] = storage.count(v.__class__)

    return (jsonify(dictionary))
