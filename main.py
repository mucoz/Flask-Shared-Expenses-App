
from app import app as application
from flask import jsonify
from jwt.exceptions import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError
import controllers.messages.messages as msg

@application.errorhandler(NoAuthorizationError)
def handle_missing_authorization_error(e):
    return jsonify(msg.ERROR_NO_AUTHENTICATION), 401


# Custom error handler for ExpiredSignatureError
@application.errorhandler(ExpiredSignatureError)
def handle_expired_signature_error(e):
    return jsonify(msg.ERROR_TOKEN_EXPIRED), 401


@application.errorhandler(404)
def not_found(error):
    return jsonify(msg.ERROR_PAGE_NOT_FOUND), 404


if __name__ == "__main__":
    application.run()
    
