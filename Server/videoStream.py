from flask import Blueprint, Flask, render_template, Response

import cv2
#import line_CV
import sys

sys.path.insert(0, "../OPEN_CV")
from Line_Detection import detect_lane

videoStreamBp = Blueprint('video_feed', __name__)

#vvalues to control with OpenCV
auto_values = {
    'speed': 0,
    'angle': 0,
}

from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False)
# Raspberry Pi camera module (requires picamera package)
values = None
def gen_frames(camera):  
    # get camera frame
    global auto_values
    while True:
        frame = camera.get_frame()
    # Su dung OpenCV cua Khanh o day de return ra angle
        savedImage = cv2.imwrite("saved-test-image.jpg",frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('saved-test-image.jpg', 'rb').read() + b'\r\n\r\n')

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
