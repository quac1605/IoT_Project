import numpy as np 
import cv2
import sys




def display_lines(frame, lane_lines, line_color=(0, 255, 0), line_width=2):
    line_image = np.zeros_like(frame)
    if lane_lines is not None:
        for line in lane_lines:
                cv2.line(line_image, (line[0],line[1]), (line[2],line[3]), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image

abc = display_lines(frame,lane_lines,line_color=(0,255,0), line_width=2)    

#lane_lines_image = display_lines(frame, line_image)
cv2.imshow("lane lines", abc)
cv2.waitKey(0)


