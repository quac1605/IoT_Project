import sys
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control")
import KeyBoardRecogniton as kp
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control//DC_Motor")
import Backward as bw
import Forward as fw
import Stop as stop
import time
kp.init()
x=50
y=50

while True:
    if x<100:
        if kp.getKey('UP'):
            x = x + 5
            print(x)
            time.sleep(1)
    else:
        if kp.getKey('UP'):
            x=100
             fw.run(x)
    if x != 0:
        if kp.getKey('w'):
            print('w')
            stop.stop()
    if x<100:
        if kp.getKey('DOWN'):
            bw.run(x)
            x = x + 5
            print(x)
            time.sleep(1)
    else:
        if kp.getKey('DOWN'):
            x=100
             bw.run(x)
    if y

