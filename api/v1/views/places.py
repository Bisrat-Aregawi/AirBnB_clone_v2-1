#!/usr/bin/python3
""" Place APIRest
"""

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def places_list(city_id):
    """ list of an objetc in a dict form
    """
    lista = []
    dic = storage.all('City')
    for elem in dic:
        if dic[elem].id == city_id:
            var = dic[elem].places
            for i in var:
                lista.append(i.to_dict())
            return (jsonify(lista))
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'])
def place(place_id):
    """ list of objetc in dict form
    """
    dic = storage.all('Place')
    for elem in dic:
        if dic[elem].id == place_id:
            return (jsonify(dic[elem].to_dict()))
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def place_delete(place_id):
    """ delete the delete
    """
    dic = storage.all('Place')
    for key in dic:
        if place_id == dic[key].id:
            dic[key].delete()
            storage.save()
            return (jsonify({}))
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def add_place(city_id):
    """ create a place of a specified city
    """
    lista = []
    obj = storage.get("City", city_id)
    content = request.get_json()
    if not obj:
        abort(404)
    if not request.json:
        return (jsonify("Not a JSON"), 400)
    else:
        if "user_id" not in content.keys():
            return (jsonify("Missing user_id"), 400)
        obj2 = storage.get("User", content["user_id"])
        if not obj2:
            abort(404)
        if "name" not in content.keys():
            return (jsonify("Missing name"), 400)

        content["city_id"] = city_id
        new_place = Place(**content)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ update specified place
    """
    dic = storage.all('Place')
    for key in dic:
        if place_id == dic[key].id:
            if not request.json:
                return (jsonify("Not a JSON"), 400)
            else:
                forbidden = ["id", "update_at", "created_at",
                             "city_id", "user_id"]
                content = request.get_json()
                for k in content:
                    if k not in forbidden:
                        setattr(dic[key], k, content[k])
                dic[key].save()
                return jsonify(dic[key].to_dict())
    abort(404)
