import sys
sys.path.insert(0, "//home//pi//Desktop//IoT_Project//Modul//Motor_Control")
import Control as ctrl
import KeyBoardRecogniton as kw
from time import sleep
speed = 0
angle = 0
kw.init()
while True:
    if (speed < -100):
        speed = -100
    elif (speed > 100):
        speed = 100

    if (angle < -100):
        angle = -100
    elif (angle > 100):
        angle = 100


    if kw.getKey('UP'):
        speed=speed+5
    elif kw.getKey('DOWN'):
        speed=speed-5

    print('speed:',speed)
    if kw.getKey('LEFT'):
        angle=angle-20
    elif kw.getKey('RIGHT'):
        angle=angle+20

    ctrl.speed(speed)
    ctrl.grad(angle)
    print('angle',angle)
    sleep(0.1)

    if kw.getKey('p'):
        speed = 0
        angle = 0