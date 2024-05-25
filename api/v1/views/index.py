#!/usr/bin/python3
"""create  a flask app: app_views"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """returns a JSON response for RESTFUL API health"""
    resp = {'status': "OK"}
    return jsonify(resp)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """return: json of all objs"""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }

    return jsonify(stats)
