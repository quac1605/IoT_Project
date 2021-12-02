from flask import Flask, render_template, Response, request, redirect, url_for
from flask_socketio import SocketIO
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
speed = 0
angle = 0

pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

# App Globals (do not edit)
sio = socketio.Server(async_mode='threading')
app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)


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


# try to control throw keyboard behavior
def control_loop():
    global speed
    global angle
    while True:
        ctrl.speed(int(speed))
        ctrl.grad(int(angle))
        print("speed:  ", speed)
        print("angle:  ", angle)
        sleep(0.08)

def thread1(threadname, q1,q2):
    #read variable "a" modify by thread 2
    global speed
    global angle
    while True:
        #speed = q1.get()
        #angle = q2.get()
        if speed is None: return # Poison pill
        #ctrl.speed(int(speed))
        print("speed in control_thread",speed)
        if angle is None: return
        #ctrl.grad(int(angle))
        print("angle in control_thread",angle)
        sleep(0.08)

thread1 = Thread( target=thread1, args=("Thread-1", speed_queue,angle_queue) )


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
    app.run(host='0.0.0.0', debug=False)
    thread1.join()
