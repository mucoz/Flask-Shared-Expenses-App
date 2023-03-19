from flask import Blueprint, jsonify, request
from models.user import User
from flask_jwt_extended import jwt_required
from database import db
import controllers.messages.messages as msg

user_blueprint = Blueprint('users', __name__)


@user_blueprint.route("/", methods=["GET"])
@jwt_required()
def get_users():
    try:
        users = User.query.all()
        output=[]
        for user in users:
            user_data = {}
            user_data["id"] = user.id
            user_data["name"] = user.name
            user_data["location"] = user.location
            output.append(user_data)
        return jsonify(msg.SEND_DATA(output)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500

@user_blueprint.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify(msg.ERROR_ITEM_NOT_FOUND)
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['location'] = user.location
        events_data = []
        for event in user.events:
            event_data = {}
            event_data['id'] = event.id
            event_data['name'] = event.name
            #event_data['attendees'] = event.attendees
            event_data['user_id'] = event.user_id
            events_data.append(event_data)
        user_data['events'] = events_data
        return jsonify(msg.SEND_DATA(user_data)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@user_blueprint.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND)
    try:
        data = request.get_json()
        user.name = data["name"]
        user.email = data["email"]
        user.location = data["location"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES)

    try:
        db.session.commit()
        return jsonify(msg.SUCCESS_UPDATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify(msg.SUCCESS_DELETED), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500
