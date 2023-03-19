from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.routes import auth_blueprint, user_blueprint, \
    event_blueprint, attendee_blueprint, expense_blueprint, \
    checkout_blueprint, sendmail_blueprint
from database import db
from config import Config
from flask_mail import Mail

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

with app.app_context():
    db.create_all()
