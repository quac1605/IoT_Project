import numpy as np 
import cv2
import sys


def detection_edges(frame):
	#import piture

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	'''
	#blue range 1
	lower_white = np.array([105, 140, 12])
	upper_white = np.array([164, 255, 107])
	'''
	#blue range dark
	lower_white = np.array([50, 75, 0])
	upper_white = np.array([165, 255, 255])
	#mask erstellen
	mask = cv2.inRange(hsv,lower_white,upper_white)
	'''
	#define white range
	lower_white = np.array([0, 0, 140])
	upper_white = np.array([179, 50, 255])
	'''
	#detection edges of lines
	edges = cv2.Canny(mask, 200, 400)

	return edges



	