import cv2
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np
import sys

sys.path.insert(0, "../OPEN_CV")
from Line_Detection import detect_lane

auto_values = {
    'speed': 0,
    'angle': 0,
}
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
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        combine_value = detect_lane(frame)
        auto_values['speed'] = combine_value['speed']
        if (combine_value['angle'] - auto_values['angle'] >= 10):
            auto_values['angle'] = auto_values['angle'] + 10;
        elif (combine_value['angle'] - auto_values['angle'] <= -10):
            auto_values['angle'] = auto_values['angle'] - 10;

        
        
        return jpeg.tobytes()