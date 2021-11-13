import numpy as np 
import cv2
import matplotlib.pyplot as plt

#import piture
frame = cv2.imread('./line.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



#define white range
lower_white = np.array([0,0,0])
upper_white = np.array([0,0,255])

#mask erstellen
mask = cv2.inRange(hsv,lower_white,upper_white)


#detection edges of lines
edges = cv2.Canny(mask, 200, 400)

#cutting image
height,width = edges.shape
mask = np.zeros_like(edges) #Return an array of zeros with the same shape and type as a given array

polygon = np.array([[
	(0,height * 1/2),
	(width,height * 1/2),
	(width,height),
	(0,height),
	]],np.int32)

cv2.fillPoly(mask, pts = [polygon], color=(255,255,255))
cropped_edges = cv2.bitwise_and(edges, mask)


#detect line segment
rho = 1  # distance precision in pixel, i.e. 1 pixel
angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
min_threshold = 10  # minimal of votes
line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, #output: only points
                                    np.array([]), minLineLength=8, maxLineGap=4)

#drawing line 

#ok ok
cv2.imshow("Input",cropped_edges)
cv2.waitKey(0)