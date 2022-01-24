from flask import Flask, render_template, Response, request, make_response
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from time import sleep
from threading import Thread, Lock
import cv2
import sys

sys.path.insert(0, "..//Modul//Motor_Control")
import Control as ctrl

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app)
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
from camera_pi import auto_values

#Add Streaming Video to this Web throw Blueprint
from videoStream import videoStreamBp
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
    print(message)

def OnchangedValue(lastValue,nowvalue,Socketio):
    if(lastValue['angle'] != nowvalue['angle'] or lastValue['speed'] != nowvalue['speed']):
            Socketio.emit('Sever updated value', { 'who': 'speed', 'data': nowvalue['speed'] }, broadcast=True, namespace='/control')
            Socketio.emit('Sever updated value', { 'who': 'angle', 'data': nowvalue['angle'] }, broadcast=True, namespace='/control')
    
"""Create Another Thread to Control the Car"""
def thread1(threadname, val):
    global control_values
    global auto_values
    global socketio
    while True:
        #auto mode
        if (control_values['mode'] == 'auto'):
            OnchangedValue(control_values,auto_values,socketio)
            control_values['angle'] = auto_values['angle']
            control_values['speed'] = auto_values['speed']
            #print('auto set angle = ',auto_values['angle'], 'auto set speed = ', auto_values['speed'])    
        ctrl.speed(int(control_values['speed']))
        ctrl.grad(int(control_values['angle']))      
        sleep(0.1)


thread1 = Thread( target=thread1, args=("Thread-1", control_values) )

if __name__ == '__main__':
    thread1.start()
    socketio.run(app,host='0.0.0.0', port=5000, debug=False)
    thread1.join()