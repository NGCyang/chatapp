from flask import Flask, json, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#mysql://username:password@host:port/database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yangmeng123@localhost/chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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

'''
Intital
'''
def setup_app(app):
   db.create_all()


'''
Router
'''
@app.route('/')
def main():
    return "Chat App"

# /signup/?name=value
@app.route('/signup',methods=['POST'])
def signup():
    try:
        _user_name = request.form.get('user_name', '')
        _password = request.form.get('password', '')
        new_user = User.query.filter_by(user_name=_user_name).first()
        if new_user is None:
            new_user = User(_user_name, _password)
            db.session.add(new_user)
            db.session.commit()
            return json.dumps({'message':'New user successfully created!', 'user_id': new_user.id})
        else:
         return "User already exist!"
    except Exception as e:
        return json.dumps({'error':str(e)})


@app.route('/login',methods = ['POST', 'GET'])
def login():
    return "login"

'''
send request form Formet:
sender_id:
recipient_id:
body:
'''
@app.route('/send',methods=['POST'])
def send():
    try:
        _sender_id = request.form.get('sender_id', '')
        _recipient_id = request.form.get('recipient_id', '')
        if User.query.filter_by(id=_sender_id).first() is None:
            return json.dumps({'message' : 'Invaild Message', 'Type':'Sender doesn\'t exist!'})
        if User.query.filter_by(id=_recipient_id).first() is None:
            return json.dumps({'message' : 'Invaild Message', 'Type':'Recipient doesn\'t exist!'})
        _body = request.form.get('body', '')
        new_message = Message(_sender_id, _recipient_id, _body)
        db.session.add(new_message)
        db.session.commit()
        return json.dumps({'message':'Message Successfully Sended',
                           'message_id':new_message.id,
                           'timeStamp':new_message.send_date})
    except Exception as e:
        return json.dumps({'error':str(e)})


@app.route('/fetch',methods=['GET'])
def fetch():
    _sender_id = request.args.get('sender_id', '')
    _recipient_id = request.args.get('recipient_id', '')
    if User.query.filter_by(id=_sender_id).first() is None:
        return json.dumps({'message' : 'Invaild Message', 'Type':'Sender doesn\'t exist!'})
    if User.query.filter_by(id=_recipient_id).first() is None:
        return json.dumps({'message' : 'Invaild Message', 'Type':'Recipient doesn\'t exist!'})
    _num_per_page = int(request.args.get('numperpage',''))
    _page = int(request.args.get('page',''))
    history = Message.query.filter(((Message.sender_id == _sender_id) & (Message.recipient_id==_recipient_id)) | ((Message.sender_id == _recipient_id) & (Message.recipient_id==_sender_id))).order_by(Message.send_date.desc()).paginate(_page, _num_per_page, False).items
    return render_template('message_history.html', history=history)


if __name__ == "__main__":
    setup_app(app)
    app.run('0.0.0.0', port = 8080)
