from flask import Flask, json, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Message, User, Video, Image

app = Flask(__name__)

'''
mysql://username:password@host:port/database
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:yangmeng123@localhost/chat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

'''
Intital
'''
@app.before_first_request
def create_database():
     db.create_all()

'''
Routing
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
        sender = User.query.filter_by(id=_sender_id).first()
        recipient = User.query.filter_by(id=_recipient_id).first()
        if sender is None:
            return json.dumps({'message' : 'Invaild Message', 'Type':'Sender doesn\'t exist!'})
        if recipient is None:
            return json.dumps({'message' : 'Invaild Message', 'Type':'Recipient doesn\'t exist!'})
        _body = request.form.get('body', '')
        _type = request.form.get('type', '')
        new_message = Message(_sender_id, _recipient_id, _body, _type)
        db.session.add(new_message)
        db.session.commit()
        if _type == 'image':
            new_image = Image(new_message.id, 1, 1)
            db.session.add(new_image)
        if _type == 'video':
            new_video = Video(new_message.id, 1)
            db.session.add(new_video)
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
    history = Message.query.filter(((Message.sender_id == _sender_id) & (Message.recipient_id==_recipient_id)) | ((Message.sender_id == _recipient_id) & (Message.recipient_id==_sender_id))).order_by(Message.send_date.desc())
    if 'numperpage' in request.args and 'page' in request.args:
        _num_per_page = int(request.args.get('numperpage',''))
        _page = int(request.args.get('page',''))
        history = history.paginate(_page, _num_per_page, False).items
    return render_template('message_history.html', history=history)

@app.route('/metadata', methods=['GET'])
def metadata():

    _type = request.args.get('type', '')
    _message_id = request.args.get('message_id', '')
    if _type == 'image':
        try:
            metadata = Image.query.filter(Image.message_id==_message_id).first()
            if metadata is None:
                return json.dumps({'message': 'Invaild message_id : message doesn\'t exist!'})
            else:
                return json.dumps({'message_id': metadata.message_id,
                                    'width': metadata.width,
                                    'height': metadata.height})
        except Exception as e:
            return json.dumps({'error':str(e)})
    elif _type == 'video':
        try:
            metadata = Video.query.filter(Video.message_id==_message_id).first()
            if metadata is None:
                return json.dumps({'message': 'Invaild message_id : message doesn\'t exist!'})
            else:
                return json.dumps({'message_id': metadata.message_id,
                                    'length': metadata.length})
        except Exception as e:
            return json.dumps({'error':str(e)})

if __name__ == "__main__":
    app.run('0.0.0.0', port = 8080)
