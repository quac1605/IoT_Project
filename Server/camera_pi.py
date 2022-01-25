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
check_side = 0
old_laneline = 0
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
        global check_side
        global old_laneline
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        combine_value = detect_lane(frame)
        print('combine_value ', combine_value['angle'], 'old_value', old_value, 'angle', auto_values['angle'])
        auto_values['speed'] = combine_value['speed']

        if(combine_value['lane_number'] == 2):
            check_side = 0
            if (combine_value['angle'] > 77 and (combine_value['angle'] - (auto_values['angle']/1.2) >= 8) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] < -77 and (combine_value['angle'] - (auto_values['angle']/1.2) <= -8) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 65 and (combine_value['angle']*1.2 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] <= -65 and (combine_value['angle']*1.2 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 45 and (combine_value['angle']*1.15 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] <= -45 and (combine_value['angle']*1.15 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 25 and (combine_value['angle']*1.1 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] <= -25 and (combine_value['angle']*1.1 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 4
            elif (auto_values['angle'] <= 0):
                auto_values['angle'] = auto_values['angle'] + 4
            elif (auto_values['angle'] > 0):
                auto_values['angle'] = auto_values['angle'] - 4
            old_laneline = 2
        elif(combine_value['lane_number'] == 1):
            check_side = 0
            old_laneline = 0
            if ((combine_value['angle'] >= 80) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif ((combine_value['angle'] <= -80) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 60 and (combine_value['angle']*1.33 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] <= -60 and (combine_value['angle']*1.33 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 48 and (combine_value['angle']*1.26 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 8
            elif (combine_value['angle'] <= -48 and (combine_value['angle']*1.26 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 8
            elif (combine_value['angle'] >= 25 and (combine_value['angle']*1.23 - (auto_values['angle']) >= 5) and auto_values['angle'] <= 100):
                auto_values['angle'] = auto_values['angle'] + 4
            elif (combine_value['angle'] <= -25 and (combine_value['angle']*1.23 - (auto_values['angle']) <= -5) and auto_values['angle'] >= -100):
                auto_values['angle'] = auto_values['angle'] - 4
            elif (auto_values['angle'] <= 0):
                auto_values['angle'] = auto_values['angle'] + 4
            elif (auto_values['angle'] > 0):
                auto_values['angle'] = auto_values['angle'] - 4
            old_laneline = 1
        elif(combine_value['lane_number'] == 0):
            if (old_laneline == 1 and check_side < 500 and (auto_values['angle'] > 35) or (auto_values['angle'] < -35)):
                if (check_side == 0):
                    auto_values['angle'] = -auto_values['angle']
                    check_side = check_side + 1
                else:
                    check_side = check_side + 1
            else:
                auto_values['speed'] = 0
                check_side = 0

        old_value = combine_value['angle']
        
        
        return jpeg.tobytes()