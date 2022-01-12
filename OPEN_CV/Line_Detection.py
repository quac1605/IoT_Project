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
import math
'''
#import piture
read_frame = cv2.imread('./08_12_02_pic.PNG')
frame = cv2.resize(read_frame,(480,320))

#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

height,width = frame.shape[:2]

'''

def detect_lane(frame):
	#frame = cv2.imread(frame_url)
	edges = Detection_Edges.detection_edges(frame)
	cropped_edges = Cutting_Image.cutting_image(edges)
	line_segments = Detect_Line_Segment.detect_line_segments(cropped_edges)
	lane_lines = Combine_Line_Segments.average_slope_intercept(frame, line_segments)
	#take lmid_ane_line
	if (len(lane_lines) == 2):
		first_lane_line = lane_lines[0]
		second_lane_line = lane_lines[1]
		line_image = np.zeros_like(frame)
		start_mid_line = [int((first_lane_line[0]+second_lane_line[0])/2),int((first_lane_line[1]+second_lane_line[1])/2)] #lam sao de su dung float
		end_mid_line =  [int((first_lane_line[2]+second_lane_line[2])/2),int((first_lane_line[3]+second_lane_line[3])/2)]
		
		cv2.line(line_image,(start_mid_line[0],start_mid_line[1]),(end_mid_line[0],end_mid_line[1]), (0,0,255),10)
		line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
		cv2.imwrite('video_image.jpg', line_image)
		
		#caculate angle
		x_offset = start_mid_line[0] - end_mid_line[0]
		y_offset = end_mid_line[1] - start_mid_line[1]
		print('x_offset', x_offset)
		print('y_offset', y_offset)
		if (y_offset):
			angle_to_mid_line = math.atan(x_offset/y_offset) * 180 / math.pi
		else:
			angle_to_mid_line = 0
	else:
		angle_to_mid_line = 0
	return angle_to_mid_line

'''
lane_lines = detect_lane(frame)


#lane_lines_string = ' '.join([str(item) for item in lane_lines])
first_lane_line = lane_lines[0]
second_lane_line = lane_lines[1]

line_image = np.zeros_like(frame)
'''
#cv2.line(line_image,(532,345),(610,230), (0,255,0),10)
#cv2.line(line_image,(1536,550),(1250,245), (0,255,0),10)
'''
cv2.line(line_image,(first_lane_line[0],first_lane_line[1]),(first_lane_line[2],first_lane_line[3]), (0,255,0),10)  #draw line on the right
cv2.line(line_image,(second_lane_line[0],second_lane_line[1]),(second_lane_line[2],second_lane_line[3]), (0,255,0),10) #draw line on the left
'''


#cv2.circle(line_image,(345,0), 20, (0,255,0), 2)
'''
#mid_line recognize
mid = int(width/2)
start_mid_line = [int((first_lane_line[0]+second_lane_line[0])/2),int((first_lane_line[1]+second_lane_line[1])/2)] #lam sao de su dung float
end_mid_line =  [int((first_lane_line[2]+second_lane_line[2])/2),int((first_lane_line[3]+second_lane_line[3])/2)]
'''
'''
cv2.line(line_image,(start_mid_line[0],start_mid_line[1]),(end_mid_line[0],end_mid_line[1]), (0,0,255),10)
'''
'''
#angle to mid_line
x_offset = start_mid_line[0] - end_mid_line[0]
y_offset = end_mid_line[0] - end_mid_line[1]
angle_to_mid_line = math.atan(x_offset/y_offset) * 180 / math.pi
'''

'''
line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)



#lane_lines_image = display_lines(frame, line_image)

print("Height and width of screen: ",height,width)
print("First lane line: ",first_lane_line)
print("Second lane line: ",second_lane_line)

print("\n")
print("Starting point of mid line: ",start_mid_line)
print("Ending point of mid line: ",end_mid_line)
print("Angle to mid line in grad: ",math.atan(x_offset/y_offset) * 180.0 / math.pi)


#cv2.imshow("Lane Lines",line_image)
cv2.imshow("lane lines", line_image)
#print(lane_lines)
cv2.waitKey(0)
'''