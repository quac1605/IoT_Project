from flask import Blueprint, Flask, render_template, Response

import cv2

videoStreamBp = Blueprint('video_feed', __name__)

from camera_pi import VideoCamera

# Raspberry Pi camera module (requires picamera package)
def gen_frames():  
    # get camera frame
    while True:
        pi_camera = VideoCamera(flip=False)
        frame = pi_camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
