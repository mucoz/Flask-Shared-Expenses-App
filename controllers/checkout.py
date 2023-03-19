from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import controllers.messages.messages as msg


checkout_blueprint = Blueprint('checkout', __name__)


@checkout_blueprint.route("/", methods=["POST"])
@jwt_required()
def get_debt_list():
    try:
        spending_data = request.get_json()
        # Check if the values are numeric
        for key, value in spending_data.items():
            if not isinstance(value, (int, float)):
                # Return error message if a value is not numeric
                return jsonify(msg.ERROR_MISSIN_NUMERIC), 400
        # Calculate the average spending per person
        num_people = len(spending_data)
        total_spending_amount = sum(spending_data.values())
        average_spending = total_spending_amount / num_people

        # Calculate the amount each person owes or is owed
        balance = {}
        for person, amount in spending_data.items():
            balance[person] = amount - average_spending
        debt_list = {}
        # Find who owes whom and how much
        for person1 in balance:
            for person2 in balance:
                if person1 != person2:
                    if balance[person1] > 0 and balance[person2] < 0:
                        amount = min(balance[person1], -balance[person2])
                        name = f"{person2} owes {person1} "
                        debt_list[name] = f"{amount:.2f}"
                        # print(f"{person2} owes {person1} {amount:.2f} zl")
                        balance[person1] -= amount
                        balance[person2] += amount
        if not debt_list:
            return jsonify(msg.ERROR_NOBODY_OWES), 200
        else:
            return jsonify(msg.SEND_DATA(debt_list)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500
