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

active_chat_sessions = set()

NAMESPACE ='/private'


@socketio.on('connect', namespace=NAMESPACE)
def connect():
    print('New socket session is created')


@socketio.on('authorize', namespace=NAMESPACE)
def authorize(username):
    active_users[username] = request.sid
    print(active_users)


@socketio.on('get_users', namespace=NAMESPACE)
def users():
    print('Sending users to client')
    emit('users', {'data': list(active_users.keys())}, broadcast=True)


@socketio.on('open_chat_session', namespace=NAMESPACE)
def open_chat_session(payload):
    new_chat_session = payload['source'] + ':' + payload['target']
    reversed_chat_session = payload['target'] + ':' + payload['source']
    if (new_chat_session in active_chat_sessions) or (reversed_chat_session in active_chat_sessions):
        print('Chat session is already exits')
    else:
        active_chat_sessions.add(new_chat_session)
    emit('updateChatSessions', {'data': list(active_chat_sessions)}, broadcast=True)


@socketio.on('get_open_sessions', namespace=NAMESPACE)
def get_open_sessions():
    emit('updateChatSessions', {'data': list(active_chat_sessions)})


@socketio.on('send_message', namespace=NAMESPACE)
def send_message(payload):
    send_from = payload['messageFrom']
    send_to = payload['messageTo']
    send_to_room_id = active_users[send_to]
    message = payload['message']
    print(f'Send message "{message}" from {send_from} to {send_to}')
    emit('receiveMessage', {'messageFrom': send_from, 'messageTo': send_to, 'message': send_from + ': ' + message}, room=send_to_room_id)


if __name__ == '__main__':
    socketio.run(app)
