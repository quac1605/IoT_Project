import sys
import time
# Insert the path of modules folder
sys.path.insert(0, "//home//pi//Desktop//IoT_Project//Modul//Motor_Control")

import PWM

max_angle=1.613
min_angle=1.472

def rotation(percent):
    ms = min_angle + ((max_angle - min_angle)/100*percent)
    PWM.set(ms,13)