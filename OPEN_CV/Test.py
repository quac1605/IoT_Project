import numpy as np 
import cv2
import matplotlib.pyplot as plt

#import piture
frame = cv2.imread('F:/FH_Kiel/Projekt/Autonomous_Car/OPEN_CV/line.jpeg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


#define white range
lower_blue = np.array([60,40,40])
upper_blue = np.array([150,255,255])

#mask erstellen
mask = cv2.inRange(hsv,lower_blue,upper_blue)


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


#drawing line 
def display_lines(frame, line_segments):
	line_image = np.zeros_like(frame)
	if line_segments is not None:
		for line in line_segments:
			x1, y1, x2, y2 = line.reshape(4)
			cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
	return line_image		


#detect line segment
rho = 1  # distance precision in pixel, i.e. 1 pixel
angle = np.pi / 180  # angular precision in radian, i.e. 1 degree
min_threshold = 10  # minimal of votes
line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, #output: only points
                                    np.array([]), minLineLength=8, maxLineGap=4)

line_image = display_lines(frame,line_segments)


cv2.imshow("Lane Lines", edges)
cv2.waitKey(0)