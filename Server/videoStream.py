from flask import Blueprint, Flask, render_template, Response

import cv2
#import line_CV
import sys

videoStreamBp = Blueprint('video_feed', __name__)

#avoid crash
frame = cv2.imread('saved-test-image.jpg')

from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False)
# Raspberry Pi camera module (requires picamera package)
values = None
def gen_frames(camera):  
    # get camera frame and public to global
    global frame
    while True:
        frame = camera.get_frame()
    # Su dung OpenCV cua Khanh o day de return ra angle
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
       '''
       yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('video_image.jpg', 'rb').read() + b'\r\n\r\n')
        '''
               

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(pi_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
