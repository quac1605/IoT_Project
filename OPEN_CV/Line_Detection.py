import numpy as np 
import cv2
import matplotlib.pyplot as plt
def make_points(frame, line):
    height, width, _ = frame.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]
#import piture
frame = cv2.imread('./line.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

cv2.imshow("Detect frame",hsv)

#define white range

lower_white = np.array([15,40,40])
upper_white = np.array([15,255,255])


#mask erstellen
mask = cv2.inRange(hsv,lower_white,upper_white)
cv2.imshow("Detect mask",mask)

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
cv2.imshow("Detect edges",cropped_edges)

