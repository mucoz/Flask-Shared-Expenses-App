from database import db


class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    expenses = db.relationship('Expense', backref='attendee', lazy=True, cascade='all, delete-orphan')
