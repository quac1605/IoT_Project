from flask import Blueprint, Flask, render_template, Response
from flask_cors import CORS, cross_origin

import cv2
#import line_CV
import sys

videoStreamBp = Blueprint('video_feed', __name__)
CORS(videoStreamBp)

#avoid crash

'''
from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False)
# Raspberry Pi camera module (requires picamera package)
'''
def gen_frames_edges(camera):  
    # get camera frame and public to global

    while True:
        #frame = camera.get_frame()
    # Su dung OpenCV cua Khanh o day de return ra angle
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('video_image_edges.jpg', 'rb').read() + b'\r\n\r\n')

def gen_frames():  
    # get camera frame and public to global
    while True:
    # Su dung OpenCV cua Khanh o day de return ra angle
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('video_image.jpg', 'rb').read() + b'\r\n\r\n')
               
@videoStreamBp.route('/video_edges_feed')
def video_edges_feed():
    return Response(gen_frames_edges(), mimetype='multipart/x-mixed-replace; boundary=frame')

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
