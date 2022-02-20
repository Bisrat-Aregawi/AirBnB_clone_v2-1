#!/usr/bin/python3
""" Place_reviews APIRest
"""

from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def rev_list(place_id):
    """ list of objetc in dict form
    """
    target_place = storage.get(Place, place_id)
    if target_place:
        reviews = [
            rev.to_dict() for rev in target_place.reviews
        ]
        return jsonify(reviews)
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review(review_id):
    """ list of objetc in dict form
    """
    target_review = storage.get(Review, review_id)
    if target_review:
        return jsonify(target_review.to_dict())
    abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def rev_delete(review_id):
    """ delete the delete
    """
    target_review = storage.get(Review, review_id)
    if target_review:
        target_review.delete()
        storage.save()
        storage.close()
        return jsonify({})
    abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def add_rev(place_id):
    """ create a review of a specified city
    """
    review_dict = request.get_json(silent=True)
    if review_dict:
        if review_dict.get("text"):
            if review_dict.get("user_id"):
                target_user = storage.get(User, review_dict.get("user_id"))
                if not target_user:
                    abort(404)
                target_place = storage.get(Place, place_id)
                if not target_place:
                    abort(404)
                new_review = Review(**review_dict)
                target_place.reviews.append(new_review)
                storage.save()
                storage.close()
                delattr(new_review, "place")
                return (jsonify(new_review.to_dict()), 201)
            return (jsonify(error="Missing user_id"), 400)
        return (jsonify(error="Missing text"), 400)
    return (jsonify(error="Not a JSON"), 400)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_rev(review_id):
    """ update a specified place
    """
    review_dict = request.get_json(silent=True)
    if review_dict:
        update_me = storage.get(Review, review_id)
        if update_me:
            forbidden = ["id", "update_at", "created_at", "place_id", "user_id"]
            for k, v in review_dict.items():
                if k not in forbidden:
                    setattr(update_me, k, v)
            storage.save()
            storage.close()
            return jsonify(update_me.to_dict())
        abort(404)
    return (jsonify(error="Not a JSON"), 400)
