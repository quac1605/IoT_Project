from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SERVER_NAME']='iotcar.cc:5000'
socketio = SocketIO(app)

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
    socketio.run(app, debug=True)