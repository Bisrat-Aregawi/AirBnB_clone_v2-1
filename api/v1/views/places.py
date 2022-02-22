#!/usr/bin/python3
""" Place APIRest
"""

from copy import copy
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models.state import State
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_list(city_id):
    """ list of an objetc in a dict form
    """
    target_city = storage.get(City, city_id)
    if target_city:
        places = [
            p.to_dict() for p in target_city.places
        ]
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def place(place_id):
    """ list of objetc in dict form
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        return jsonify(target_place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """ delete the delete
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        target_place.delete()
        storage.save()
        storage.close()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """ create a place of a specified city
    """
    place_dict = request.get_json(silent=True)
    if place_dict:
        if place_dict.get("name"):
            if place_dict.get("user_id"):
                target_user = storage.get(User, place_dict["user_id"])
                if not target_user:
                    abort(404)
                target_city = storage.get(City, city_id)
                if not target_city:
                    abort(404)
                new_place = Place(**place_dict)
                target_city.places.append(new_place)
                storage.save()
                storage.close()
                delattr(new_place, "cities")
                return (jsonify(new_place.to_dict()), 201)
            return (jsonify(error="Missing user_id"), 400)
        return (jsonify(error="Missing name"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ update specified place
    """
    place_dict = request.get_json(silent=True)
    if place_dict:
        update_me = storage.get(Place, place_id)
        if update_me:
            forbidden = [
                "id", "updated_at", "created_at", "city_id", "user_id"
            ]
            for k, v in place_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
            storage.save()
            storage.close()
            return jsonify(update_me.to_dict())
        abort(404)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/places_search', methods=['POST'])
def get_places():
    """Retrieve all Place objects depending on JSON in the body of request
    """
    places = []
    srchs_dct = request.get_json(silent=True)
    if srchs_dct == {}:
        for plc in list(storage.all(Place).values()):
            places.append(plc.to_dict())
        return jsonify(places)
    elif srchs_dct is not None:
        if srchs_dct.get("states"):
            for st_id in srchs_dct.get("states"):
                st = storage.get(State, st_id)
                if not st:
                    abort(404)
                for cty in st.cities:
                    places.extend(cty.places)
        if srchs_dct.get("cities"):
            for cty_id in srchs_dct.get("cities"):
                cty = storage.get(City, cty_id)
                if not cty:
                    abort(404)
                cty_plcs = cty.places
                for plc in cty_plcs:
                    if plc not in places:
                        places.append(plc)
        if srchs_dct.get("amenities"):
            if srchs_dct.get("states") is None:
                if srchs_dct.get("cities") is None:
                    places = list(storage.all(Place).values())
            plc_cpy = copy(places)
            for plc in plc_cpy:
                for am_id in srchs_dct.get("amenities"):
                    req_amen = storage.get(Amenity, am_id)
                    if not req_amen:
                        abort(404)
                    if req_amen not in plc.amenities:
                        places.remove(plc)
                        break
        storage.close()
        for plc in places:
            delattr(plc, "amenities")
        return jsonify(
            [plc.to_dict() for plc in places]
        )
    else:
        return (jsonify(error="Not a JSON"), 400)
