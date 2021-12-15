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
control_values = {
    'speed': 0,
    'angle': 0,
    'mode':'manuell'
}

#Add Streaming Video to this Web throw Blueprint
from videoStream import videoStreamBp, auto_values
app.register_blueprint(videoStreamBp)

#Create  GUI for namespace "/"
@app.route('/')
def index():
    return render_template('index.html',**control_values)
  
#Try to catch connect signal from namespace "/control"
@socketio.on('connect', namespace='/control')
def test_connect():
    print('client connected')
    emit('after connect',  {'data':'Lets dance'}, namespace='/control')

#Catch control value throw socket io in "/control", use this to set shared values to control Car and tell the User that value changed successfully 
@socketio.on('Value changed', namespace='/control')
def value_changed(message):
    global control_values
    control_values[message['who']] = message['data']
    emit('Sever updated value', message, broadcast=True, namespace='/control')
    print(message['data'])

"""Create Another Thread to Control the Car"""
def thread1(threadname, val):
    #read variable "a" modify by thread 2
    global control_values
    global auto_values
    while True:
        #auto mode
        if (control_values['mode'] == 'auto'):
            ctrl.speed(int(auto_values['speed']))
            ctrl.grad(int(auto_values['angle']))
            print(int(auto_values['angle']))
        #code for manuell
        elif (control_values['mode'] == 'manuell'):
            ctrl.speed(int(control_values['speed']))
            ctrl.grad(int(control_values['angle']))
        sleep(0.1)

thread1 = Thread( target=thread1, args=("Thread-1", control_values) )

if __name__ == '__main__':
    thread1.start()
    socketio.run(app,host='0.0.0.0', port=5000, debug=False)
    thread1.join()