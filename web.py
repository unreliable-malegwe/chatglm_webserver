from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room
from processglm import Worker
import logging
from logging.handlers import TimedRotatingFileHandler
import pymysql
import traceback
import win32api,win32con

# worker = Worker()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/regist')
def regist():
    return render_template('regist.html')

@app.route('/login')
def getLoginRequest():
    db = pymysql.connect(host="localhost", user="root", password="wwzzxx123", database="chatglm_webserver", charset="utf8")
    cursor = db.cursor()
    sql = "select * from accounts where id=" + request.args.get('id') + " and password=" + request.args.get('password')

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        if len(results) == 1:
            return render_template('index.html')
        else:
            return "账号或密码错误"
        db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    db.close()

@app.route('/regist')
def getRegistRequest():
    db = pymysql.connect(host="localhost", user="root", password="wwzzxx123", database="chatglm_webserver", charset="utf8")
    cursor = db.cursor()
    userid = request.args.get('id')
    password = request.args.get('password')
    password2 = request.args.get('password2')
    if password == password2:
        sql =  "insert into accounts(id, password) valvues ("+userid+", "+password+")"
        try:
            cursor.execute(sql)
            db.commit()
            return render_template('login.html')
        except:
            traceback.print_exc()
            db.rollback()
            return "注册失败"
        db.close()
    else:
        win32api.MessageBox(0, "两次密码不一致", "提示", win32con.MB_ICONWARNING)
        return render_template('regist.html')


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
    # response = worker.process(message)
    socketio.emit('message', message, room=request.sid)
    # app.logger.info(f'Message sent to {request.sid}: {response}')

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] {%(filename)s:%(lineno)d}[%(levelname)s][%(thread)d] - %(message)s")
    handler = TimedRotatingFileHandler('./logs/app.log', when="D", interval=1, backupCount=10, encoding='utf-8',delay=False, utc=True)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    socketio.run(app, host='127.0.0.1', port=8080)
