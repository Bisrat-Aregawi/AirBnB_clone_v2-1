#!/usr/bin/python3
""" Amenities APIRest
"""

from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'])
def amenity_list():
    """ list of objetc in dict form
    """
    amenities_list = [
        am.to_dict() for am in storage.all(Amenity)
    ]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE'])
def amenity_id(amenity_id):
    """ realize the specific action depending on a method
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        if request.method == "GET":
            return jsonify(amenity.to_dict())
        elif request.method == "DELETE":
            amenity.delete()
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/amenities', methods=['POST'])
def amenity_item():
    """ add a new item
    """
    amenity_dict = request.get_json(silent=True)
    if amenity_dict:
        if amenity_dict.get("name"):
            new_amenity = Amenity(**amenity_dict)
            new_amenity.save()
            storage.close()
            return (jsonify(new_amenity.to_dict()), 201)
        return (jsonify(error="Missing name"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ update item
    """
    amenity_dict = request.get_json(silent=True)
    if amenity_dict:
        update_me = storage.get(Amenity, amenity_id)
        if update_me:
            forbidden = ["id", "update_at", "created_at"]
            for k, v in amenity_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
                    storage.save()
                    storage.close()
                    return jsonify(update_me.to_dict())
        abort(404)
    return (jsonify(error="Not a JSON"), 400)
