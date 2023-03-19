from flask import Blueprint, request, jsonify
from models.event import Event
from database import db
from flask_jwt_extended import jwt_required
import controllers.messages.messages as msg

event_blueprint = Blueprint('events', __name__)


@event_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_events():
    try:
        events = Event.query.all()
        output = []
        for event in events:
            event_data = {}
            event_data['id'] = event.id
            event_data['name'] = event.name
            #event_data['attendees'] = event.attendees
            event_data['user_id'] = event.user_id
            output.append(event_data)
        return jsonify(msg.SEND_DATA(output)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@event_blueprint.route('/<int:event_id>', methods=['GET'])
@jwt_required()
def get_event(event_id):
    try:
        event = Event.query.get(event_id)
        if not event:
            return jsonify(msg.ERROR_ITEM_NOT_FOUND)
        event_data = {}
        event_data['id'] = event.id
        event_data['name'] = event.name
        event_data['user_id'] = event.user_id
        attendees_data = []
        for attendee in event.attendees:
            attendee_data = {}
            attendee_data['id'] = attendee.id
            attendee_data['name'] = attendee.name
            attendee_data['event_id'] = attendee.event_id
            attendees_data.append(attendee_data)
        event_data["attendees"] = attendees_data
        return jsonify(msg.SEND_DATA(event_data)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@event_blueprint.route("/last-event", methods=["GET"])
@jwt_required()
def get_lastevent():
    try:
        last_event = Event.query.order_by(Event.created_at.desc()).first()
        if last_event:
            return jsonify({'id': last_event.id, 'name': last_event.name, 'created_at': last_event.created_at})
        else:
            return jsonify(msg.ERROR_ITEM_NOT_FOUND)
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500

@event_blueprint.route("/", methods=['POST'])
@jwt_required()
def create_event():
    try:
        data = request.get_json()
        name = data["name"]
        user_id = data["user_id"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 200

    try:
        event = Event(name=name, user_id=user_id)
        db.session.add(event)
        db.session.commit()
        return jsonify(msg.SUCCESS_CREATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@event_blueprint.route('/<int:event_id>', methods=['PUT'])
@jwt_required()
def update_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 404
    try:
        data = request.get_json()
        event.name = data['name']
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 400

    try:
        db.session.commit()
        return jsonify(msg.SUCCESS_UPDATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@event_blueprint.route('/<int:event_id>', methods=['DELETE'])
@jwt_required()
def delete_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify(msg.SUCCESS_DELETED), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500
