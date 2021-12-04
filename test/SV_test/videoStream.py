from flask import Blueprint, Flask, render_template, Response

import cv2

videoStreamBp = Blueprint('video_feed', __name__)

from camera_pi import VideoCamera
# Raspberry Pi camera module (requires picamera package)
def gen_frames(camera):  
    while True:
        success, frame = camera.get_frame()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@videoStreamBp.route('/video_feed')
def video_feed():
    return Response(gen_frames(VideoCamera(flip=False)), mimetype='multipart/x-mixed-replace; boundary=frame')
