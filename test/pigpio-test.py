import sys
import time
# Insert the path of modules folder
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control")

import PWM

max_speed = 1.3
min_speed = 1.47

def forward(percent):
    ms = min_speed + ((max_speed - min_speed)/100*percent)
    PWM.set(ms)

for x in range (0,101,1):
   print(x)
   forward(x)
   time.sleep(1)
