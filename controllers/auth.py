from flask import Blueprint, request, jsonify
from models.user import User
from models.event import Event
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import controllers.messages.messages as msg

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/register", methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data["name"]
        email = data["email"]
        password = data["password"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 400

    try:
        user = User.find_by_mail(email)
        if user:
            return jsonify(msg.ERROR_USER_EXISTS), 400
        hashed_pass = generate_password_hash(password, method='sha256')
        new_user = User(name=name, email=email, password=hashed_pass)
        db.session.add(new_user)
        db.session.commit()
        #generate token
        token = create_access_token(identity=new_user.email)
        return jsonify(msg.SEND_REGISTRATION_MESSAGE(new_user.id, new_user.email, token)), 200
    except:
        return jsonify(msg.ERROR_INTERNAL_SERVER), 500

@auth_blueprint.route("/login", methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        email = data["email"]
        password = data["password"]
    except:
        return jsonify(msg.ERROR_MISSING_VALUES), 400

    try:
        user = User.find_by_mail(email)
        if not user:
            return jsonify(msg.ERROR_INVALID_USER), 401
        if not check_password_hash(user.password, password):
            return jsonify(msg.ERROR_INVALID_USER), 401
        # generate token
        token = create_access_token(identity=user.email)
        return jsonify(msg.SEND_LOGIN_MESSAGE(user.id, user.email, token)), 200
    except:
         return jsonify(msg.ERROR_INTERNAL_SERVER), 500
