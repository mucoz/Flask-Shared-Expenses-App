from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.routes import auth_blueprint, user_blueprint, \
    event_blueprint, attendee_blueprint, expense_blueprint, \
    checkout_blueprint, sendmail_blueprint
from database import db
from config import Config
from flask_mail import Mail
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError
import controllers.messages.messages as msg


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mail = Mail(app)
jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(auth_blueprint, url_prefix='/api/v1/auth')
app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(event_blueprint, url_prefix='/api/v1/events')
app.register_blueprint(attendee_blueprint, url_prefix='/api/v1/attendees')
app.register_blueprint(expense_blueprint, url_prefix='/api/v1/expenses')
app.register_blueprint(checkout_blueprint, url_prefix='/api/v1/checkout')
# app.register_blueprint(sendmail_blueprint, url_prefix='/api/v1/sendmail')


@app.errorhandler(NoAuthorizationError)
def handle_missing_authorization_error(e):
    return jsonify(msg.ERROR_NO_AUTHENTICATION), 401


# Custom error handler for ExpiredSignatureError
@app.errorhandler(ExpiredSignatureError)
def handle_expired_signature_error(e):
    return jsonify(msg.ERROR_TOKEN_EXPIRED), 401


@app.errorhandler(404)
def not_found(error):
    return jsonify(msg.ERROR_PAGE_NOT_FOUND), 404


with app.app_context():
    db.create_all()
