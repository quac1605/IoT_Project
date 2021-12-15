import cv2
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np
import sys

sys.path.insert(0, "../OPEN_CV")
from Line_Detection import detect_lane

auto_values = {
    'speed': 60,
    'angle': 0,
}
i = 0
test = 0
class VideoCamera(object):
    global auto_values
    def __init__(self, resolution=(480,320), framerate=120,flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(1.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        global i
        global test
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        #auto_values['angle'] = -(detect_lane(frame) * 0.8)
        if (i == 10):
            auto_values['angle'] = (test/10)
            print(auto_values['angle'])
            i= 0
            test = 0
        else:
            cc, frame = detect_lane(frame)
            test = test + cc
            i = i + 1
        #return jpeg.tobytes()
        return frame