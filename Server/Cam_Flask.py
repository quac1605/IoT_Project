from time import sleep
import sys
from camera import VideoCamera
import time
import threading
import os
sys.path.insert(0, "//home//pi//Desktop//IoT_Project//Modul//Motor_Control")
import Control as ctrl
from flask import Flask, render_template, Response, request, redirect, url_for

speed = 0
angle = 0

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
"""
@app.route("/online_control/<speed>/<angle>")
def online_control(speed,angle):
        #ctrl.speed(speed)
        #ctrl.grad(angle)
        print(speed)
        print(angle)
        return 0
"""
@app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)
