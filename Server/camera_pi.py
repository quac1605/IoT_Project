import cv2
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np
import sys

sys.path.insert(0, "../OPEN_CV")
from Line_Detection import detect_lane

class VideoCamera(object):
    def __init__(self, resolution=(480,320), framerate=120,flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        #savedImage = cv2.imwrite("saved-test-image.jpg",frame)
        detect_lane(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()