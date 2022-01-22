import numpy as np 
import cv2
import sys

def cutting_image(edges):
	height,width = edges.shape
	mask = np.zeros_like(edges) #Return an array of zeros with the same shape and type as a given array

	polygon = np.array([[
		(0,height * 0.55),
		(width,height * 0.55),
		(width,height),
		(0,height),
		]],np.int32)

	cv2.fillPoly(mask, pts = [polygon], color=(255,255,255))
	cropped_edges = cv2.bitwise_and(edges, mask)

	return cropped_edges