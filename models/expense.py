from database import db


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    explanation = db.Column(db.String(250), nullable=False)
    attendee_id = db.Column(db.Integer, db.ForeignKey('attendee.id'))
    amount = db.Column(db.Float, nullable=True)
