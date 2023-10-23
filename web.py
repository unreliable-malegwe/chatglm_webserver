from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from processglm import Worker
import logging
from logging.handlers import TimedRotatingFileHandler

worker = Worker()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    join_room(request.sid)
    app.logger.info(f'Client connected: {request.sid}')

@socketio.on('disconnect')
def handle_disconnect():
    leave_room(request.sid)
    app.logger.info(f'Client disconnected: {request.sid}')

@socketio.on('message')
def handle_message(message):
    app.logger.info(f'Message received from {request.sid}: {message}')
    response = worker.process(message)
    socketio.emit('message', response, room=request.sid)
    app.logger.info(f'Message sent to {request.sid}: {response}')

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(filename)s:%(lineno)d}[%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler('./logs/app.log', when="D", interval=1, backupCount=10, encoding='utf-8',delay=False, utc=True)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    socketio.run(app, host='127.0.0.1', port=8080)
