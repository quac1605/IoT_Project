import numpy as np 
import cv2
import sys


def detection_edges(frame):
	#import piture
	frame = cv2.imread('F:/FH_Kiel/Projekt/Autonomous_Car/OPEN_CV/line_3.jpg')
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



	#define white range
	lower_white = np.array([123, 116, 116])
	upper_white = np.array([186, 172, 160])

	#mask erstellen
	mask = cv2.inRange(hsv,lower_white,upper_white)


	#detection edges of lines
	edges = cv2.Canny(mask, 200, 400)

	return edges



	