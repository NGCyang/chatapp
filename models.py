from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(50))
    #sender_name = db.Column(db.String(50))
    recipient_id = db.Column(db.String(50))
    #recipient_name = db.Column(db.String(50))
    body = db.Column(db.Text)
    send_date = db.Column(db.DateTime)

    #category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __init__(self, sender_id, recipient_id, body, send_date=None):
        self.sender_id = sender_id
        #self.sender_name = sender_name
        self.recipient_id = recipient_id
        #self.recipient_name = recipient_name
        self.body = body
        if send_date is None:
            send_date = datetime.utcnow()
        self.send_date = send_date

    def __repr__(self):
        return '<Post %r>' % self.body


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    password =  db.Column(db.String(50))

    def __init__(self, name, password):
        self.user_name = name
        self.password = password

    def __repr__(self):
        return '<Category %r>' % self.id
