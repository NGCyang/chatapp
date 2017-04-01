from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50))
    #sender_name = db.Column(db.String(50))
    recipient_id = db.Column(db.String(50))
    #recipient_name = db.Column(db.String(50))
    body = db.Column(db.Text)
    send_date = db.Column(db.DateTime)
    #content = posts = db.relationship('Post', backref='author', lazy='dynamic')
    message_type = db.Column(db.String(5))

    #sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))



    def __init__(self, sender_id, recipient_id, body, message_type, send_date=None):
        self.sender_id = sender_id
        #self.sender_name = sender_name
        self.recipient_id = recipient_id
        #self.recipient_name = recipient_name
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
    #send_messages = db.relationship('Message', backref='sender', lazy='dynamic')
    #recipient_messages = db.relationship('Message', backref='recipient', lazy='dynamic')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password

    def __repr__(self):
        return '<Category %r>' % self.id
