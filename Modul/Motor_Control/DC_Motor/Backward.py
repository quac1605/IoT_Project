import sys
import time
# Insert the path of modules folder
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control")

import PWM

max_speed = 1.36
min_speed = 1.46

def run(percent):
    ms = min_speed + ((max_speed - min_speed)/100*percent)
    PWM.set(ms,12)