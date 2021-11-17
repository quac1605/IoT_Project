import sys
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control//DC_Motor")
sys.path.insert(0, "//home//pi//Desktop//CAR//Modul//Motor_Control//Schritt_Motor")
import Backward as bw
import Forward as fw
import Left as lf
import Right as rt

#function to set ward
def speed(percent):
    #control about percent;
    if (percent < -100):
        percent = -100
    elif (percent > 100):
        percent = 100

    #ward
    if (percent > 0 ):
        fw.run(percent)
    else:
        bw.run(-percent)

def grad(percent):
    #control about percent;
    if (percent < -100):
        percent = -100
    elif (percent > 100):
        percent = 100

    if (percent > 0 ):
        lf.rotation(-percent)
    else:
        rt.rotation(percent)