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


def detect_lane(frame):
	edges = Detection_Edges.detection_edges(frame)
	cropped_edges,height = Cutting_Image.cutting_image(edges)
	line_segments = Detect_Line_Segment.detect_line_segments(cropped_edges)
	lane_lines = Combine_Line_Segments.average_slope_intercept(frame, line_segments)
	cv2.imwrite('video_image_edges.jpg', cropped_edges)
	cv2.imwrite('video_image.jpg', frame)
	#take lmid_ane_line
	if (len(lane_lines) == 2):
		speed_set = 45
		first_lane_line = lane_lines[0]
		second_lane_line = lane_lines[1]

		line_image = np.zeros_like(frame)
		if((first_lane_line[2] - first_lane_line[0] < -750) or (first_lane_line[2] - first_lane_line[0] > 750) or (second_lane_line[2] - second_lane_line[0] < -750) or (second_lane_line[2] - second_lane_line[0] > 750)):
			print('2 line detected (with 1 fake line)')
			lane_number = 1;
		else:
			print('2 line detected')
			lane_number = 2;
		if ((first_lane_line[2] - first_lane_line[0] < -750) or (first_lane_line[2] - first_lane_line[0] > 750)):
			x_offset = second_lane_line[2] - second_lane_line[0]
			y_offset = second_lane_line[3] - second_lane_line[1]
			#y_offset = y_offset / abs(y_offset) * height * 0.35
			angle_to_mid_line = -(math.atan(x_offset/y_offset) * 180 / math.pi)
		elif ((second_lane_line[2] - second_lane_line[0] < -750) or (second_lane_line[2] - second_lane_line[0] > 750)):
			x_offset = first_lane_line[2] - first_lane_line[0]
			y_offset = first_lane_line[3] - first_lane_line[1]
			#y_offset = y_offset / abs(y_offset) * height * 0.35
			angle_to_mid_line = -(math.atan(x_offset/y_offset) * 180 / math.pi)
		else:			
			start_mid_line = [int((first_lane_line[0]+second_lane_line[0])/2),int((first_lane_line[1]+second_lane_line[1])/2)] #lam sao de su dung float
			end_mid_line =  [int((first_lane_line[2]+second_lane_line[2])/2),int((first_lane_line[3]+second_lane_line[3])/2)]
			'''			
			#add line
			cv2.line(line_image,(start_mid_line[0],start_mid_line[1]),(end_mid_line[0],end_mid_line[1]), (0,0,255),10)
			line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
			cv2.imwrite('video_image.jpg', line_image)
			'''
			#caculate angle
			x_offset = end_mid_line[0] - start_mid_line[0]
			y_offset = end_mid_line[1] - start_mid_line[1]
			y_offset = y_offset / abs(y_offset) * height * 0.35
			angle_to_mid_line = -(math.atan(x_offset/y_offset) * 180 / math.pi)
	elif (len(lane_lines) == 1):
		speed_set = 45
		lane_number = 1;
		first_lane_line = lane_lines[0]
		print('only lane detected ')
		print(first_lane_line)
		x_offset = first_lane_line[2] - first_lane_line[0]
		y_offset = first_lane_line[3] - first_lane_line[1]
		#y_offset = y_offset / abs(y_offset) * height * 0.35
		angle_to_mid_line = -(math.atan(x_offset/y_offset) * 180 / math.pi)
		#fking crashing avoid
		if (x_offset <  -750 or x_offset > 750):
			angle_to_mid_line = -angle_to_mid_line

	else:
		print('no lane detected')
		lane_number = 0;
		cv2.imwrite('video_image.jpg', frame)
		speed_set = 0
		angle_to_mid_line = 0
	return {'speed':speed_set, 'angle':angle_to_mid_line, 'lane_number':lane_number}
