from database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(50), nullable=True)
    events = db.relationship('Event', backref='user', lazy=True, cascade='all, delete-orphan')

    def create(self):
        db.session.add(self)
        db.session.commit(self)
        return self

    @classmethod
    def find_by_mail(cls, email):
        return cls.query.filter_by(email=email).first()
