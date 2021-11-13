import numpy as np 
import cv2


def detection_edges(frame):
	#import piture
	frame = cv2.imread('F:/FH_Kiel/Projekt/Autonomous_Car/line.jpg')
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



	#define white range
	lower_white = np.array([0,0,0])
	upper_white = np.array([0,0,255])

	#mask erstellen
	mask = cv2.inRange(hsv,lower_white,upper_white)


	#detection edges of lines
	edges = cv2.Canny(mask, 200, 400)

	return edges


	