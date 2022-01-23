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

old_value = 0
class VideoCamera(object):
    global auto_values
    global old_value
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
        global old_value
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        combine_value = detect_lane(frame)
        print('combine_value ', combine_value['angle'], 'old_value', old_value, 'angle', auto_values['angle'])
        auto_values['speed'] = combine_value['speed']
        '''
        if ((combine_value['angle'] - old_value >= 12) and auto_values['angle'] <= 100):
            auto_values['angle'] = auto_values['angle'] + 20;
        elif ((combine_value['angle'] - old_value <= -12) and auto_values['angle'] >= -100):
            auto_values['angle'] = auto_values['angle'] - 20;
        '''
        if(combine_value['lane_number'] == 2):
            if ((combine_value['angle'] - (auto_values['angle']/3) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 10
            elif ((combine_value['angle'] - (auto_values['angle']/3) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 10
        elif(combine_value['lane_number'] == 1):
            if ((combine_value['angle'] >= 50) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 10
            elif ((combine_value['angle'] <= -45) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 10
            elif ((auto_values['angle'] >= 0)):
                auto_values['angle'] = auto_values['angle'] - 5
            elif ((auto_values['angle'] < 0)):
                auto_values['angle'] = auto_values['angle'] + 5
        elif(combine_value['lane_number'] == 0):
                auto_values['angle'] = 0

        old_value = combine_value['angle']
        
        
        return jpeg.tobytes()