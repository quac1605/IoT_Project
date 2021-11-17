import numpy as np 
import cv2
import matplotlib.pyplot as plt
import sys
sys.path.insert(0,"..\OPEN_CV")
import Detection_Edges
import Cutting_Image
import Detect_Line_Segment
import Combine_Line_Segments
import f_make_point
import logging

#import piture
frame = cv2.imread('F:/FH_Kiel/Projekt/Autonomous_Car/OPEN_CV/line_3.jpg')
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

lower_blue = np.array([20, 20, 20])
upper_blue = np.array([255, 255, 255])

#mask erstellen
mask = cv2.inRange(hsv,lower_blue,upper_blue)



def detect_lane(frame):
	edges = Detection_Edges.detection_edges(frame)
	cropped_edges = Cutting_Image.cutting_image(edges)
	line_segments = Detect_Line_Segment.detect_line_segments(cropped_edges)
	lane_lines = Combine_Line_Segments.average_slope_intercept(frame, line_segments)

	return cropped_edges

detect_lane(frame)

cv2.imshow("abc", mask)
cv2.waitKey(0)