from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO, emit
from threading import Lock
import cv2
from imutils.video.pivideostream import PiVideoStream
app = Flask(__name__)
socketio = SocketIO(app)

"""
from videoStream import videoStreamBp
app.register_blueprint(videoStreamBp)
"""

values = {
    'speed': 0,
    'angle': 0,
}

camera = PiVideoStream().start()  # use 0 for web camera
#  for cctv camera use rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' instead of camera
# for local webcam use cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
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
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

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
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)