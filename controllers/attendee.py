from flask import Blueprint, request, jsonify
from models.attendee import Attendee
from database import db
from flask_jwt_extended import jwt_required
import controllers.messages.messages as msg

attendee_blueprint = Blueprint('attendees', __name__)


@attendee_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_attendees():
    try:
        attendees = Attendee.query.all()
        output = []
        for attendee in attendees:
            attendee_data = {}
            attendee_data['id'] = attendee.id
            attendee_data['name'] = attendee.name
            # attendee_data['expenses'] = attendee.expenses
            attendee_data['event_id'] = attendee.event_id
            output.append(attendee_data)
        return jsonify(msg.SEND_DATA(output)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@attendee_blueprint.route('/<int:attendee_id>', methods=['GET'])
@jwt_required()
def get_attendee(attendee_id):
    try:
        attendee = Attendee.query.get(attendee_id)
        if not attendee:
            return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
        attendee_data = {}
        attendee_data['id'] = attendee.id
        attendee_data['name'] = attendee.name
        attendee_data['event_id'] = attendee.event_id
        expenses_data = []
        for expense in attendee.expenses:
            expense_data = {}
            expense_data["id"] = expense.id
            expense_data["explanation"] = expense.explanation
            expense_data["amount"] = expense.amount
            expense_data["attendee_id"] = expense.attendee_id
            expenses_data.append(expense_data)
        attendee_data["expenses"] = expenses_data
        return jsonify(msg.SEND_DATA(attendee_data)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@attendee_blueprint.route("/", methods=['POST'])
@jwt_required()
def create_attendee():
    try:
        data = request.get_json()
        name = data["name"]
        event_id = data["event_id"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 400

    try:
        attendee = Attendee(name=name, event_id=event_id)
        #event.create()
        db.session.add(attendee)
        db.session.commit()
        return jsonify(msg.SUCCESS_CREATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@attendee_blueprint.route("/<int:attendee_id>", methods=['PUT'])
@jwt_required()
def update_attendee(attendee_id):
    attendee = Attendee.query.filter_by(id=attendee_id).first()
    if not attendee:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        data = request.get_json()
        attendee.name = data["name"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 400

    try:
        db.session.commit()
        return jsonify(msg.SUCCESS_UPDATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@attendee_blueprint.route("/<int:attendee_id>", methods=["DELETE"])
@jwt_required()
def delete_item(attendee_id):
    attendee = Attendee.query.filter_by(id=attendee_id).first()
    if not attendee:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        db.session.delete(attendee)
        db.session.commit()
        return jsonify(msg.SUCCESS_DELETED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500
