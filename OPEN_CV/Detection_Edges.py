import numpy as np 
import cv2
import sys


def detection_edges(frame):
	#import piture

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#green range normal
	lower = np.array([50, 28, 110])
	upper = np.array([95, 255, 255])
	
	mask = cv2.inRange(hsv,lower,upper)
	#detection edges of lines
	edges = cv2.Canny(mask, 200, 400)

	return edges



	