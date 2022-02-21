#!/usr/bin/python3
"""Place and Amenity M2M RESTful API setup module"""

from models import storage
from models.place import Place
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def am_list(place_id):
    """Respond to GET request to a place's amenities

    Args:
        place_id (str): uuid of place

    Returns:
        list of amenities for a place with id `place_id`
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        amenities = [
            am.to_dict() for am in target_place.amenities
        ]
        return jsonify(amenities)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def am_delete(place_id, amenity_id):
    """Delete a place's amenitiy from database

    Args:
        place_id (str): uuid of place
        amenity_id (str): uuid of an amenity record to delete

    Returns:
        empty json on success
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
    """Link an amenity to a place

    Args:
        place_id (str): uuid of place
        amenity_id (str): uuid of an amenity record

    Returns:
        Linked amenity on success
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
