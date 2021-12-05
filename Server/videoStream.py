from flask import Blueprint, Flask, render_template, Response

import cv2

videoStreamBp = Blueprint('video_feed', __name__)

test_values = {
    'speed' : 0,
    "angle" : 0,
}

from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False)
# Raspberry Pi camera module (requires picamera package)
values = None
def gen_frames(camera):  
    # get camera frame
    global test_values
    while True:
        frame = camera.get_frame()
        if (int(test_values['speed']) > 50):
            print("test ++++++++++++++++++++")
        elif (int(test_values['speed']) < (-50)) :
            print("test -----------------")   
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
