#!/usr/bin/python3
""" User APIRest
"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'])
def user_list():
    """ list of an objetc in a dict form
    """
    users_list = [
        usr.to_dict() for usr in storage.all(User).values()
    ]
    return (jsonify(users_list))


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE'])
def user_id(user_id):
    """ realize the specific action depending on method
    """
    user = storage.get(User, user_id)
    if user:
        if request.method == "GET":
            return jsonify(user.to_dict())
        elif request.method == "DELETE":
            user.delete()
            storage.save()
            storage.close()
            return jsonify({})
    abort(404)


@app_views.route('/users', methods=['POST'])
def user_item():
    """ add a new item
    """
    user_dict = request.get_json(silent=True)
    if user_dict:
        if user_dict.get('email'):
            if user_dict.get('password'):
                new_user = User(**user_dict)
                new_user.save()
                storage.close()
                return (jsonify(new_user.to_dict()), 201)
            return (jsonify(error="Missing password"), 400)
        return (jsonify(error="Missing email"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ update an item
    """
    user_dict = request.get_json(silent=True)
    if user_dict:
        update_me = storage.get(User, user_id)
        if update_me:
            forbidden = ["id", "email", "created_at", "updated_at"]
            for k, v in user_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
            storage.save()
            storage.close()
            return jsonify(update_me.to_dict())
        abort(404)
    return (jsonify(error="Not a JSON"), 400)
