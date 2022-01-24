from flask import Blueprint, Flask, render_template, Response
from flask_cors import CORS, cross_origin
from time import sleep

import cv2
#import line_CV
import sys

videoStreamBp = Blueprint('video_feed', __name__)
CORS(videoStreamBp)

from camera_pi import VideoCamera
pi_camera = VideoCamera(flip=False)
frame = pi_camera.get_frame()
#avoid crash


# Raspberry Pi camera module (requires picamera package)

def gen_frames_edges():  
    # get camera frame and public to global
    sleep(0.1)
    global frame
    while True:
    # Su dung OpenCV cua Khanh o day de return ra angle
        frame = pi_camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('video_image_edges.jpg', 'rb').read() + b'\r\n\r\n')

def gen_frames():  
    # get camera frame and public to global
    sleep(0.1)
    global frame
    while True:
    # Su dung OpenCV cua Khanh o day de return ra angle
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
               
@videoStreamBp.route('/video_edges_feed')
def video_edges_feed():
    return Response(gen_frames_edges(), mimetype='multipart/x-mixed-replace; boundary=frame')

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
