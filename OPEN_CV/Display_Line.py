import numpy as np 
import cv2
import sys

frame = cv2.imread('F:/FH_Kiel/Projekt/Autonomous_Car/OPEN_CV/line.jpeg')

def display_lines(frame, lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

lane_lines_image = display_lines(frame, line_image)
cv2.imshow("lane lines", lane_lines_image)