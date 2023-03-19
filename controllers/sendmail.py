from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import controllers.messages.messages as msgs
from flask_mail import Mail, Message


sendmail_blueprint = Blueprint('sendmail', __name__)

mail = Mail()


@sendmail_blueprint.route('/', methods=['POST'])
@jwt_required()
def send_mail():
    try:
        to = request.json['to']
        subject = request.json['subject']
        body = request.json['body']
        if not to or not subject or not body:
            return jsonify(msgs.ERROR_MISSING_VALUES), 400
        msg = Message(subject, recipients=[to])
        msg.body = body
        mail.send(msg)
        return jsonify({"message": 'Email sent successfully.', "status": "success"})
    except:
        return jsonify(msgs.ERROR_INTERNAL_SERVER), 500
