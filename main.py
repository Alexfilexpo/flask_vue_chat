import eventlet
from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS

eventlet.monkey_patch()
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)

active_users = {}

NAMESPACE ='/private'


@socketio.on('connect', namespace=NAMESPACE)
def connect():
    print('New socket session is created')


@socketio.on('authorize', namespace=NAMESPACE)
def authorize(username):
    active_users[username] = request.sid


@socketio.on('get_users', namespace=NAMESPACE)
def users():
    emit('users', {'data': list(active_users.keys())}, broadcast=True)


@socketio.on('send_message', namespace=NAMESPACE)
def send_message(payload):
    send_from = payload['messageFrom']
    send_to = payload['messageTo']
    send_to_room_id = active_users[send_to]
    message = payload['message']
    print(f'Send message "{message}" to {send_to} from {send_from}')
    emit('receiveMessage', {'messageFrom': send_from, 'messageTo': send_to, 'message': message}, room=send_to_room_id)


if __name__ == '__main__':
    socketio.run(app)
