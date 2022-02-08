#!/usr/bin/python3
""" City APIRest
 careful by default it uses get method
"""

from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def list_cities(state_id):
    """ list all cities from a specified state
    """
    target_state = storage.get(State, state_id)
    if target_state:
        cities = [
            ct.to_dict() for ct in target_state.cities
        ]
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'])
def city_id(city_id):
    """ return the city
    """
    target_city = storage.get(City, city_id)
    if target_city:
        return jsonify(target_city.to_dict())
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def city_delete(city_id):
    """ delete the delete
    """
    target_city = storage.get(City, city_id)
    if target_city:
        target_city.delete()
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def add_city(state_id):
    """ create a city of a specified state
    """
    city_dict = request.get_json(silent=True)
    if city_dict:
        if city_dict.get("name"):
            target_state = storage.get(State, state_id)
            if not target_state:
                abort(404)
            new_city = City(**city_dict)
            target_state.cities.append(new_city)
            storage.save()
            storage.close()
            delattr(new_city, "state")
            return (jsonify(new_city.to_dict()), 201)
        return (jsonify(error="Missing name"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ update specified city
    """
    update_me = storage.get(City, city_id)
    if update_me:
        city_dict = request.get_json(silent=True)
        if city_dict:
            forbidden = ["id", "update_at", "created_at", "state_id"]
            for k, v in city_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
                    storage.save()
                    storage.close()
                    return jsonify(update_me.to_dict())
        return (jsonify(error="Not a JSON"), 400)
    abort(404)
