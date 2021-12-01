import sys
import pigpio

def ms2percent(x_ms):
    return int((x_ms / 20)*1000000) ;


pi = pigpio.pi()

def set(a,GPIO_PINNUMBER):
    if not pi.connected:
       exit()

    #print("a = ",a)
    pi.hardware_PWM(GPIO_PINNUMBER, 50, ms2percent(float(a)))