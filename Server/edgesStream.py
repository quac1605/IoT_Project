from flask import Blueprint, Flask, render_template, Response
from flask.ext.cors import CORS, cross_origin

import cv2
#import line_CV
import sys

edgesStreamBp = Blueprint('video_edges_feed', __name__)
CORS(edgesStreamBp)
# Raspberry Pi camera module (requires picamera package)

def gen_frames_edges():  
    # get camera frame and public to global
    while True:
    # Su dung OpenCV cua Khanh o day de return ra angle
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + open('video_image_edges.jpg', 'rb').read() + b'\r\n\r\n')
  
               
@edgesStreamBp.route('/video_edges_feed')
def video_feed():
    return Response(gen_frames_edges(), mimetype='multipart/x-mixed-replace; boundary=frame')