import sys
import time
# Insert the path of modules folder
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control")

import PWM


def stop():
    PWM.set(1.46,12)

stop()