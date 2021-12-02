from flask import Flask, render_template, Response, request, redirect, url_for
from flask_socketio import SocketIO, emit
from threading import Thread
from queue import Queue
import os
from time import sleep
import sys
from camera import VideoCamera
import time
import threading

sys.path.insert(0, "//home//pi//Desktop//IoT_Project//Modul//Motor_Control")
import Control as ctrl

"""
speed_queue = Queue()
angle_queue = Queue()
"""

pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)
socketio = SocketIO(app);
values = {
    'speed': 0,
    'angle': 0,
}
"""
socketio = SocketIO(app, async_mode='eventlet')
import eventlet
eventlet.monkey_patch()
"""

@app.route('/')
def index():
    return render_template('index.html')


def gen(camera):
    # get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})

@socketio.on('Value changed')
def value_changed(message):
    global values
    values[message['who']] = message['data']
    emit('update value', message, broadcast=True)
    print(message['data'])
# try to control throw keyboard behavior
def control_loop():
    global values
    while True:
        ctrl.speed(int(values['speed']))
        ctrl.grad(int(values['angle']))
        print("speed:  ", values['speed'])
        print("angle:  ", values['speed'])
        sleep(0.1)

def thread1(threadname, val):
    #read variable "a" modify by thread 2
    global values
    while True:
        #speed = q1.get()
        #angle = q2.get()
        if values['speed'] is None: return # Poison pill
        #ctrl.speed(int(speed))
        print("speed in control_thread",values['speed'])
        if angle is None: return
        #ctrl.grad(int(angle))
        print("angle in control_thread",values['angle'])
        sleep(0.1)

thread1 = Thread( target=thread1, args=("Thread-1", values) )


@app.route('/online_control', methods=['POST'])
def online_control():
    global speed
    global angle
    speed = request.form['speed']
    angle = request.form['angle']
    #speed_queue.put( speed)
    #angle_queue.put( angle);
    #print("online control speed received: ",speed)
    #print("online control angle received",angle)
    return ("",204)


"""
@app.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@app.route('/online_control', methods=['POST', 'GET'])
def online_control():
    if request.method == 'POST':
        user = request.form['nm']
        print(user)
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))
"""

if __name__ == '__main__':
    #_thread.start_new_thread(control_loop, (speed,angle))
    thread1.start()
    socketio.run(app, host='0.0.0.0', debug=False)
    thread1.join()
