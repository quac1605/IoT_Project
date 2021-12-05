from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Lock

app = Flask(__name__)
#for socket
socketio = SocketIO(app, async_mode='eventlet')
import eventlet
eventlet.monkey_patch()
#thread = None
thread1 = None
thread_lock = Lock()



from videoStream import videoStreamBp
app.register_blueprint(videoStreamBp)

values = {
    'speed': 0,
    'angle': 0,
}

@app.route('/')
def index():
    return render_template('index.html',**values)
  
@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('Value changed')
def value_changed(message):
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(message['data'])


if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000, debug=True)