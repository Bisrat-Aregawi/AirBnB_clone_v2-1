#!/usr/bin/python3
""" Place_amenities Restful API
"""

from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review
from api.v1.views import app_views
from models.place import place_amenity
from flask import jsonify, abort, request
from os import getenv

type = getenv('HBNB_TYPE_STORAGE')


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def am_list(place_id):
    """ list of an objetc in dict form
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        amenities = [
            am.to_dict() for am in target_place.amenities
        ]
        return jsonify(amenities)
    abort(404)


@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE']
)
def am_delete(place_id, amenity_id):
    """ delete the object
    """
    target_place = storage.get(Place, place_id)
    if not target_place:
        abort(404)
    target_amenity = storage.get(Amenity, amenity_id)
    if not target_amenity:
        abort(404)
    if target_amenity not in target_place.amenities:
        abort(404)
    target_amenity.delete()
    storage.save()
    storage.close()
    return jsonify({})


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def add_am(place_id, amenity_id):
    """ create an amenity of a city
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        target_amenity = storage.get(Amenity, amenity_id)
        if target_amenity:
            if target_amenity in target_place.amenities:
                return jsonify(target_amenity.to_dict())
            target_place.amenities.append(target_amenity)
            storage.save()
            storage.close()
            return (jsonify(target_amenity.to_dict()), 201)
        abort(404)
    abort(404)
