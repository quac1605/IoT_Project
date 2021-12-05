from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread, Lock
import sys

sys.path.insert(0, "//home//pi//Desktop//IoT_Project//Modul//Motor_Control")
import Control as ctrl

app = Flask(__name__)
#for socket
socketio = SocketIO(app, async_mode='threading')
#thread = None
thread1 = None
thread_lock = Lock()

#Datas to control Car
values = {
    'speed': 0,
    'angle': 0,
}

#Add Streaming Video to this Web throw Blueprint
from videoStream import videoStreamBp
app.register_blueprint(videoStreamBp)

#Create  GUI for namespace "/"
@app.route('/')
def index():
    return render_template('index.html',**values)
  
#Try to catch connect signal from namespace "/control"
@socketio.on('connect', namespace='/control')
def test_connect():
    print('client connected')
    emit('after connect',  {'data':'Lets dance'}, namespace='/control')

#Catch control value throw socket io in "/control", use this to set shared values to control Car and tell the User that value changed successfully 
@socketio.on('Value changed', namespace='/control')
def value_changed(message):
    global values
    values[message['who']] = message['data']
    emit('Sever updated value', message, broadcast=True, namespace='/control')
    print(message['data'])

"""Create Another Thread to Control the Car"""
def thread1(threadname, val):
    #read variable "a" modify by thread 2
    global values
    while True:
        if values['speed'] is None: return # Poison pill
        #ctrl.speed(int(values['speed']))
        #print("speed in control_thread",values['speed'])
        if values['angle'] is None: return
        #ctrl.grad(int(values['angle']))
        #print("angle in control_thread",values['angle'])
        sleep(0.1)

thread1 = Thread( target=thread1, args=("Thread-1", values) )

if __name__ == '__main__':
    thread1.start()
    socketio.run(app,host='0.0.0.0', port=5000, debug=False)
    thread1.join()