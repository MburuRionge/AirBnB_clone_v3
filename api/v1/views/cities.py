#!/usr/bin/python3
"""
route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_city(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/states/<state_id>', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """
    create city route
    param: state_id - state id
    :return: newly created city obj
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, atate_id)
    if not state:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing name')
    data['state_id'] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """
    gets a specific City object by ID
    :param city_id: city object id
    :return: city obj with the specified id or error
    """

    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
    return abort(404)


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    updates specific City object by ID
    :param city_id: city object ID
    :return: city object and 200 on success, or 400 or 404 on failure
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not requset.get_json():
            return abort(400, 'Not a JSON')

        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key,value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    deletes City by id
    :param city_id: city object id
    :return: empty dict with 200 or 404 if not found
    """

    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)
