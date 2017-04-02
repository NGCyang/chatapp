from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    recipient_id = db.Column(db.Integer)
    body = db.Column(db.Text)
    send_date = db.Column(db.DateTime)
    message_type = db.Column(db.String(5))

    def __init__(self, sender_id, recipient_id, body, message_type, send_date=None):
        self.sender_id = sender_id
        self.recipient_id = recipient_id
        self.body = body
        self.message_type = message_type
        if send_date is None:
            send_date = datetime.utcnow()
        self.send_date = send_date

    def __repr__(self):
        return '<Post %r>' % self.body

class Image(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)

    def __init__(self, message_id, width, height):
        self.message_id = message_id
        self.width = width
        self.height = height

    def __repr__(self):
        return '<Post %r>' % self.message_id

class Video(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Integer)

    def __init__(self, message_id, length):
        self.message_id = message_id
        self.length = length

    def __repr__(self):
        return '<Post %r>' % self.message_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    password =  db.Column(db.String(50))

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return '<Category %r>' % self.id
