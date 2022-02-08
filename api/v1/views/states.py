#!/usr/bin/python3
""" State APIRest
"""

from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'])
def list_dict():
    """ list of an objetc in a dict form
    """
    states_list = [
        st.to_dict() for st in storage.all('State').values()
    ]
    return (jsonify(states_list))


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE'])
def state_id(state_id):
    """ realize the specific action depending on method
    """
    state = storage.get(State, state_id)
    if state:
        if request.method == "GET":
            return jsonify(state.to_dict())
        elif request.method == "DELETE":
            state.delete()
            storage.save()
            return jsonify({})
    abort(404)


@app_views.route('/states', methods=['POST'])
def add_item():
    """ add a new item
    """
    state_dict = request.get_json(silent=True)
    if state_dict:
        if state_dict.get('name'):
            new_state = State(**state_dict)
            new_state.save()
            return (jsonify(new_state.to_dict()), 201)
        return (jsonify(error="Missing name"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_item(state_id):
    """ update item
    """
    update_me = storage.get(State, state_id)
    if update_me:
        state_dict = request.get_json(silent=True)
        if state_dict:
            forbidden = ["id", "update_at", "created_at"]
            for k, v in state_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
                    storage.save()
                    return jsonify(update_me.to_dict())
        return (jsonify(error="Not a JSON"), 400)
    abort(404)
