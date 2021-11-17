import numpy as np 
import cv2
import sys


def make_points(frame,line):
	height, width, _ = frame.shape
	slope, intercept = line

	y1 = height
	y2 = int(y1 * 1/2)


	x1 = max(-width, min(2* width, int((y1 - intercept) / slope )))
	x2 = max(-width, min(2* width, int((y2 - intercept) / slope )))

	return [[x1, y1, x2, y2]]