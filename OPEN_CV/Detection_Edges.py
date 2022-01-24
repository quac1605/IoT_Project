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
	'''
	#blue range dark
	lower_white = np.array([50, 75, 0])
	upper_white = np.array([165, 160, 160])
	'''
	'''
	#blue range normal
	lower_blue = np.array([102, 75, 0])
	upper_blue = np.array([140, 255, 255])
	#mask erstellen
	'''
	#green range normal
	lower = np.array([45, 33, 127])
	upper = np.array([88, 255, 255])
	mask = cv2.inRange(hsv,lower,upper)
	'''
	#define white range
	lower_white = np.array([0, 0, 140])
	upper_white = np.array([179, 50, 255])
	'''
	#detection edges of lines
	edges = cv2.Canny(mask, 200, 400)

	return edges



	