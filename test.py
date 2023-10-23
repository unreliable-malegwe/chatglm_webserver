import logging
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

# 配置日志记录
# logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] - %(message)s')
log_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
log_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s"))
app.logger.addHandler(log_handler)
app.logger.setLevel(logging.INFO)


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
    socketio.emit('message', message, room=request.sid)
    app.logger.info(f'Message received from {request.sid}: {message}')

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=8080)
