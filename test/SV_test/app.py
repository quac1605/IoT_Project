from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Lock
import cv2

import time
import cv2

app = Flask(__name__)
socketio = SocketIO(app)


from videoStream import videoStreamBp
app.register_blueprint(videoStreamBp)
"""
from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False) 
"""
values = {
    'speed': 0,
    'angle': 0,
}

"""
def gen(camera):
    # get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
"""

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
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)