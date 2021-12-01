from flask import Flask, render_template, Response, request, redirect, url_for
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


queue = Queue()
pi_camera = VideoCamera(flip=False)  # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)


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
    while True:
        global speed;
        global angle;
        ctrl.speed(int(speed))
        ctrl.grad(int(angle))
        print("speed:  ", speed)
        print("angle:  ", angle)
        sleep(0.1)

def thread1(threadname, q):
    #read variable "a" modify by thread 2
    while True:
        a = q.get()
        if a is None: return # Poison pill
        print(a)

thread1 = Thread( target=thread1, args=("Thread-1", queue) )


@app.route('/online_control', methods=['POST'])
def online_control():
    speed = request.form['speed']
    angle = request.form['angle']
    queue.put( speed)
    print(speed)
    print(angle)
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
