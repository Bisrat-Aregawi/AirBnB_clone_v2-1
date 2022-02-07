#!/usr/bin/python3
"""Module handles all RESTful API actions on state"""
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', methods=['GET'])
def states_list():
    """Return a list of states in DB.
    """
    lst = [
        state.to_dict() for state in storage.all(State).values()
    ]
    return jsonify(lst)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_with_id(state_id):
    """Return state record with id `state_id` from DB

    Args:
        state_id (str): uuid of state requred

    Returns:
        Jsonified version of state record with id `state_id`
    """
    try:
        return jsonify(storage.get(State, state_id).to_dict())
    except Exception:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_state_with_id(state_id):
    """Delete state record with id `state_id` from DB.

    Args:
        state_id (str): uuid of state required

    Returns:
        Empty jsonified dictionary upon success
    """
    try:
        marked_obj = storage.get(State, state_id)
        storage.delete(marked_obj)
        storage.save()
        return jsonify({})
    except Exception:
        abort(404)


@app_views.route('/states', methods=['POST'])
def add_state():
    """Insert a new state to DB

    Args:
        None

    Returns:
        Jsonified new_state created
    """
    if not request.get_json(silent=True):
        return (jsonify(error="Not a JSON"), 400)
    if request.get_json().get('name'):
        new_state = State(**request.get_json())
        new_state.save()
        return (jsonify(new_state.to_dict()), 201)
    return (jsonify(error="Missing name"), 400)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update state with id `state_id` in DB

    Args:
        state_id (str): uuid of state requred

    Returns:
        Jsonified state record and 200 status code
        If request is not valid JSON 400 with error message 'NOT a JSON'
    """
    if not request.get_json(silent=True):
        abort(400)
    update_state = storage.get(State, state_id)
    if update_state:
        dictionary = request.get_json()
        for k, v in dictionary.items():
            if k != 'created_at' and k != 'updated_at' and k != 'id':
                setattr(update_state, k, v)
                storage.save()
                return (jsonify(update_state.to_dict()), 200)
    else:
        abort(404)
