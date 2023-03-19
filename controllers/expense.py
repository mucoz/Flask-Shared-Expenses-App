from flask import Blueprint, request, jsonify
from models.expense import Expense
from models.attendee import Attendee
from database import db
from flask_jwt_extended import jwt_required
import controllers.messages.messages as msg

expense_blueprint = Blueprint('expenses', __name__)


@expense_blueprint.route('/total/<int:event_id>', methods=['GET'])
@jwt_required()
def get_total_expenses(event_id):
    try:
        total =db.session.query(Attendee.name, db.func.sum(Expense.amount)).\
        join(Expense).filter(Attendee.event_id==event_id).\
        group_by(Attendee.name).all()
        response = {}
        for name, total_expenses in total:
            response[name] = round(total_expenses, 2)

        return jsonify(msg.SEND_DATA(response)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500

@expense_blueprint.route('/total_person/<int:attendee_id>', methods=['GET'])
@jwt_required()
def get_total_person(attendee_id):
    try:
        total = db.session.query(db.func.sum(Expense.amount)).filter_by(attendee_id=attendee_id).scalar()
        return jsonify(msg.SEND_DATA(total)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@expense_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_expenses():
    try:
        expenses = Expense.query.all()
        output=[]
        for expense in expenses:
            expense_data = {}
            expense_data['id'] = expense.id
            expense_data['explanation'] = expense.explanation
            expense_data['amount'] = expense.amount
            expense_data['attendee_id'] = expense.attendee_id
            output.append(expense_data)
        return jsonify(msg.SEND_DATA(output)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@expense_blueprint.route('/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    try:
        expense = Expense.query.get(expense_id)
        if not expense:
            return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
        expense_data = {}
        expense_data["id"] = expense.id
        expense_data["explanation"] = expense.explanation
        expense_data["amount"] = expense.amount
        expense_data["attendee_id"] = expense.attendee_id
        return jsonify(msg.SEND_DATA(expense_data)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@expense_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_expense():
    try:
        data = request.get_json()
        explanation = data["explanation"]
        amount = data["amount"]
        attendee_id = data["attendee_id"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 200

    try:
        expense = Expense(explanation=explanation, amount=amount, attendee_id=attendee_id)
        db.session.add(expense)
        db.session.commit()
        return jsonify(msg.SUCCESS_CREATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@expense_blueprint.route('/<int:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id).first()
    if not expense:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        data = request.get_json()
        expense.explanation = data["explanation"]
        expense.amount = data["amount"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES)
    try:
        db.session.commit()
        return jsonify(msg.SUCCESS_UPDATED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500


@expense_blueprint.route("/<int:expense_id>", methods=["DELETE"])
@jwt_required()
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id).first()
    if not expense:
        return jsonify(msg.ERROR_ITEM_NOT_FOUND), 400
    try:
        db.session.delete(expense)
        db.session.commit()
        return jsonify(msg.SUCCESS_DELETED), 201
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500
