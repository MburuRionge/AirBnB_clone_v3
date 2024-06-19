#!/usr/bin/python3
"""
route for handling place and amenities linking
"""
from flask import jsonify, abort
from os import getenv
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    get all amenities of a place
    :param place_id: amenity id
    :return: all amenities
    """
    fetched_obj = storage.get(Place, (place_id))

    if fetched_obj is None:
        abort(404)

    all_amenities = [obj.to_json() for obj in fetched_obj.amenities]

    return jsonify(all_amenities)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(place_id, amenity_id):
    """
    unlinks an amenity in a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: empty dict or error
    """
    fetched_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not fetched_obj or not amenity_obj:
        abort(404)

    found = False

    for obj in fetched_obj.amenities:
        if obj.id == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                fetched_obj.amenities.remove(obj)
            else:
                fetched_obj.amenity_ids.remove(obj.id)
            fetched_obj.save()
            found = True
            break

    if not found:
        abort(404)
    return jsonify({})


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """
    fetched_obj = storage.get(Place, place_id)
    amenity_obj = storage.get(Amenity, amenity_id)

    if not fetched_obj or not amenity_obj:
        abort(404)

    if amenity_obj in fetched_obj.amenities:
        return jsonify(amenity_obj.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        fetched_obj.amenities.append(amenity_obj)
    else:
        fetched_obj.amenity_ids.append(amenity_obj.id)

    fetched_obj.save()

    resp = jsonify(amenity_obj.to_json())
    resp.status_code = 201

    return resp
