import numpy as np 
import cv2
import sys
import logging
sys.path.insert(0,"..\OPEN_CV")
import f_make_point


def average_slope_intercept(frame, line_segments):
	lane_lines = []
	if line_segments is None:
		logging.info('No line_segments detected')
		return lane_lines

	height, width, _ = frame.shape
	left_fit = []
	right_fit = []
 
	boundary = 1/3		#ranh gioi
	left_region_boundary = width * (1 - boundary)
	right_region_boundary = width * boundary

	for line_segment in line_segments:
		for x1, y1, x2, y2 in line_segment:
			if x1 == x2:
				logging.info('skipping vertikal line segment (slope = inf): %s' % line_segment)
				continue
			fit = np.polyfit((x1,x2), (y1,y2), 1)  #duong thang y = mx + c --> m = fit[0], c = fit[1]  
			slope = fit[0]
			intercept = fit[1]
			if slope < 0:
				if x1 < left_region_boundary and x2 < left_region_boundary:
					left_fit.append((slope, intercept))

			else: 
				if x1 > right_region_boundary and x2 > right_region_boundary:
					right_fit.append((slope,intercept))

	left_fit_average = np.average(left_fit, axis = 0)
	if len(left_fit) > 0: 
		lane_lines.append(f_make_point.make_points(frame, left_fit_average))

	right_fit_average = np.average(right_fit, axis = 0)
	if len(right_fit) > 0:
		lane_lines.append(f_make_point.make_points(frame, right_fit_average))

	logging.debug('lane lines: %s' %lane_lines)
	
	return lane_lines									
