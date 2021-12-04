from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Lock
import cv2

import time
import cv2

app = Flask(__name__)
#for socket
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)
#thread = None
thread1 = None
thread_lock = Lock()


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
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


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
    socketio.run(host='0.0.0.0', port=5000, ddebug=True, threaded=True)